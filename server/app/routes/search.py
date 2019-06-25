# -- coding:UTF-8 --
from flask import request, json
from flask_login import current_user,login_user,logout_user, login_required
from app import app,db
from app.models import Template,Answer
from app.models import User,Task,Receiver,receivers
from app.utils.trans import UserToJson, TaskToJson

json_true = json.dumps('succeed')
json_false = json.dumps('failed')
'''
查看发布的任务（无需登录）返回task id:
如果有post一个user的id，则查询该id发布的任务,
若无post一个id则查询登录的user的任务
如果无id且无登录，则返回false
'''
@app.route('/task/mysponsor', methods=['GET', 'POST'])
def my_sponsor_task():
    if request.method == 'POST':
        #获取要查询的对象（当前user或者user的id）
        json_data = json.loads(request.data)
        if 'id' in json_data:
            user = User.query.filter_by(id=json_data['id']).first()
        elif current_user.is_active:
            user = current_user
        else:
            print('query error!')
            return json.dumps({'errmsg': '用户不存在'})
        
        #返回
        data = {'task_number': len(user.sponsor_tasks), 'task_id': []}
        for task in user.sponsor_tasks:
            # print(task.id)
            # now = json.dumps(task, default=TaskToJson)
            # data[0][str(i)] = now
            # i = i+1
            data['task_id'].append(task.id)

        return json.dumps(data , sort_keys=False)
    
    return json.dumps({'errmsg': '没有使用POST请求'})

'''
查看接受的任务（需要登录）
只能查询当前登录的所有接受任务
'''
@app.route('/task/myreceive', methods=['GET', 'POST'])
@login_required
def my_receive_task():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'id' in json_data:
            receivers = Receiver.query.filter_by(uid=json_data['id']).all()
        elif current_user.is_active:
            receivers = Receiver.query.filter_by(uid=current_user.id).all()
        else:
            print('query error')
            return json.dumps({'errmsg': '用户不存在'})
        #返回
        data = {'task_number': len(receivers), 'task_id': []}
        for rec in receivers:
            data['task_id'].append(rec.tid);
        return json.dumps(data, sort_keys=False)

        # return json.dumps({'errmsg': '没有传递id'})
    
    return json.dumps({'errmsg': '没有使用POST请求'})


# 任务广场的推荐
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    json_data = json.loads(request.data)
    batch_size = 5
    if 'batch_size' in json_data:
        batch_size = json_data['batch_size']
    task_list = Task.query.order_by(-Task.received_number).limit(batch_size).all()
    data = {"task_number":len(task_list), "task_info": []}
    for task in task_list:
        current = {'id': task.id, 'title': task.title, 'detail': task.detail, 'type': task.type}
        data['task_info'].append(current)
    return json.dumps(data, sort_keys=False)


# 按发布者用户名进行搜索任务
'''
接受一个包含'sponsor'属性的json 'sponsor':sponsor_name
查询指定的sponsor发起的任务
返回指定sponsor发起的所有任务的id
如果没有改sponsor则返回 json_false

返回json的
{'task_number': 2
'task_id':[1,2]
}
'''

@app.route('/search/sponsor', methods=['GET', 'POST'])
def search_by_sponsor():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'sponsor' in json_data:
            # tasks = Task.query.all()
            task_list = User.query.filter_by(username=json_data['sponsor']).first().sponsor_tasks
        else:
            print('no match result')
            return json.dumps({'errmsg': '没有传递sponsor'})

        #正确查询之后返回json
        data = {'task_number':len(task_list), 'task_id':[]}
        for task in task_list:
            data['task_id'].append(task.id)
        return json.dumps(data, sort_keys=False)

    return json.dumps({'errmsg': '没有使用POST请求'})

#按标题内容进行模糊搜索
'''
接受一个包含'key_word'属性的json 'key_word':key_word
根据key_word对任务标题进行模糊匹配
返回符合条件所有任务的id
如果没有则返回 json_false

返回json的
{'task_number': 2
'task_id':[1,2]
}
'''


@app.route('/search/title_key_word', methods=['GET', 'POST'])
def search_by_title():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'key_word' in json_data:
            key = '%' + json_data['key_word'] + '%'
            task_list = db.session.query(Task).filter(Task.title.like(key)).all()
        else:
            print('no match result')
            return json.dumps({'errmsg': '没有传递key_word'})

        #正确查询之后返回json
        data = {'task_number':len(task_list), 'task_id':[]}
        for task in task_list:
            data['task_id'].append(task.id)
        return json.dumps(data, sort_keys=False)

    return json.dumps({'errmsg': '没有使用POST请求'})


#按任务详情进行模糊搜索
'''
接受一个包含'key_word'属性的json 'key_word':key_word
根据key_word对任务详情进行模糊匹配
返回符合条件所有任务的id
如果没有则返回 json_false

返回json的
{'task_number': 2
'task_id':[1,2]
}
'''
@app.route('/search/detail_key_word', methods=['GET', 'POST'])
def search_by_detail():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'key_word' in json_data:
            key = '%' + json_data['key_word'] + '%'
            task_list = db.session.query(Task).filter(Task.detail.like(key)).all()
        else:
            print('no match result')
            return json.dumps({'errmsg': '没有传递key_word'})

        # 正确查询之后返回json
        data = {'task_number':len(task_list), 'task_id':[]}
        for task in task_list:
            data['task_id'].append(task.id)
        return json.dumps(data, sort_keys=False)

    return json.dumps({'errmsg': '没有使用POST请求'})


# 按指定id查询任务
'''
接收一个包含'task_id'属性的json
返回对应task的详情
'''
@app.route('/search/task_id', methods=['GET', 'POST'])
def getTask_by_id():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'task_id' in json_data:
            task = Task.query.filter_by(id=json_data['task_id']).first()
            if task==None:
                return json.dumps({'errmsg': '不存在该任务'})
            data = {'id':task.id, 'title':task.title, 'type':task.type,
                    'start_time':task.start_time, 'end_time':task.end_time,
                    'pay':task.pay, 'detail':task.detail, 'receiver_limit':task.receiver_limit,
                    'received_number':task.received_number, 'finished_number':task.finished_number,
                    'extra_content':task.extra_content, 'sponsor_id':task.sponsor.id,
                    'sponsor':task.sponsor.username, 'template_id':task.template.id}
            receivers_id = []
            for rec in task.receivers:
                receivers_id.append(rec.id)
            data['receivers'] = receivers_id
            return json.dumps(data, sort_keys=False)

        else:
            print('no task_id')
            return json.dumps({'errmsg': '没有传递task_id'})

    return json.dumps({'errmsg': '没有使用POST请求'})


# 按id查询用户
'''
接收一个包含‘user_id’属性的json
返回对应的用户详情的json
'''
@app.route('/search/user_id', methods=['GET', 'POST'])
def getUser_by_id():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'user_id' in json_data:
            user = User.query.filter_by(id=json_data['user_id']).first()
            if user==None:
                return json.dumps({'errmsg': '不存在该用户'})
            data = {'id':user.id, 'username':user.username, 'email':user.email, 'school':user.school,
                    'major':user.major, 'phone':user.phone, 'wx_number':user.wx_number, 'hobbit':user.hobbit, 'profile': user.profile}

            return json.dumps(data, sort_keys=False)
        return json.dumps({'errmsg': '没有传递user_id'})
    return json.dumps({'errmsg': '没有使用POST请求'})


'''
按id查询问卷模板
接收的json格式应包含 ‘template_id’属性
'''
@app.route('/search/template_id', methods=['POST'])
def getTemplate_by_id():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'template_id' in json_data:
            template = Template.query.filter_by(id=json_data['template_id']).first()
            if template == None:
                return json.dumps({'errmsg': '没有该模板'})
            data = {'id': template.id,
                    'questions': template.questions,
                    'options': template.options,
                    'types': template.types,
                    }

            return json.dumps(data, sort_keys=False)
        return json.dumps({'errmsg': '没有传递template_id'})
    return json.dumps({'errmsg': '没有使用POST请求'})


'''
根据任务接收者user_id和任务id查询问卷答案
'''
@app.route('/search/answer', methods=['POST'])
def getAnswer_by_id():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'task_id' in json_data:
            if 'user_id' in json_data:
                rec = Receiver.query.filter_by(uid=json_data['user_id'], tid=json_data['task_id']).first()
                if rec==None:
                    return json.dumps({'errmsg': '没有这个任务或者该用户没有接受该任务'})
                ans = rec.answers.answers

                data = {'answers': ans}
                return json.dumps(data, sort_keys=False)

            return json.dumps({'errmsg': '没有传递user_id'})
        return json.dumps({'errmsg': '没有传递task_id'})
    return json.dumps({'errmsg': '没有使用POST请求'})
