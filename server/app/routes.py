# -- coding:UTF-8 --
from flask import render_template, redirect, url_for, request, json
from flask_login import current_user,login_user,logout_user, login_required
from app import app,db
from app.models import Template,Answer
from app.models import User,Task,Receiver,receivers
from app.trans import UserToJson, TaskToJson

json_true = json.dumps('succeed')
json_false = json.dumps('failed')

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

'''
接受账号密码和其他个人信息

验证格式（前端）
如果未重复，存入数据库
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
	json_data = json.loads(request.data)
	users = User.query.all()
	for user in users:
		if user.id == json_data['id']:
			print('user is existed!')
			return json.dumps({'errmsg': '用户已存在'})
	user = User(id = json_data['id'], 
		username = json_data['username'], 
		email = json_data['email'] if 'email' in json_data else None, 
		school = json_data['school'] if 'school' in json_data else None, 
		major = json_data['major'] if 'major' in json_data else None, 
		phone = json_data['phone'] if 'phone' in json_data else None, 
		wx_number = json_data['wx_number'] if 'wx_number' in json_data else None, 
		hobbit = json_data['hobbit'] if 'hobbit' in json_data else None,
		profile = json_data['profile'] if 'profile' in json_data else None
		)
	user.set_password(json_data['password'])
	db.session.add(user)
	db.session.commit()
	print('register user {}!'.format(user))
	return json_true

'''
登入
接收账号密码,验证账户是否正确

正确则返回用户信息，错误则返回错误信息
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if current_user.is_authenticated:
			print('Error, user is active!')
			return json.dumps({'errmsg': '用户已登陆'})
		json_data = json.loads(request.data)
		# print(json_data)
		user = User.query.filter_by(id=json_data['id']).first()
		if user is None or not user.check_password(json_data['password']):
			print('username or password isn\'t correct!')
			return json.dumps({'errmsg': '用户名或密码错误'})
		login_user(user, remember=True)
		print('login user {}!'.format(user))
		return json.dumps(user, default=UserToJson, sort_keys=False) 
	return json.dumps({'errmsg': '没有使用POST请求'})

#登出
@app.route('/logout')
@login_required
def logout():
	logout_user()
	print('logout user succeed!')
	return json_true

'''
发布任务（需登录）
接收新建任务的所有需求信息，以当前登录user进行发布
'''
@app.route('/task/sponsor', methods=['GET', 'POST'])
@login_required
def sponsor_task():
	if request.method == 'POST':
		if current_user.is_authenticated:
			#获得post来的task数据
			json_data = json.loads(request.data)
			if 'title' not in json_data:
				return json.dumps({'errmsg': '没有传递title'})
			task = Task(
				title = json_data['title'],
				sponsor = current_user,
				type = json_data['type'] if 'type' in json_data else 'query',
				# start_time = json_data['start_time'] if 'start_time' in json_data else None,
				# end_time = json_data['end_time'] if 'end_time' in json_data else None,
				pay = json_data['pay'] if 'pay' in json_data else 0,
				detail = json_data['detail'] if 'detail' in json_data else None,
				receiver_limit = json_data['receiver_limit'] if 'receiver_limit' in json_data else 1,
				received_number = json_data['received_number'] if 'received_number' in json_data else 0,
				extra_content = json_data['extra_content'] if 'extra_content' in json_data else None			)

			task.template = Template()
			task.template.questions = json_data['questions'] if 'questions' in json_data else []
			task.template.options = json_data['options'] if 'options' in json_data else []
			task.template.types = json_data['types'] if 'types' in json_data else []
			
			db.session.add(task)
			db.session.commit()

			return json.dumps(task.id)

	return json.dumps({'errmsg': '没有使用POST请求'})

'''
接受任务(需登录）
接收任务的tid，以当前user进行接收
'''
@app.route('/task/receive', methods=['POST'])
@login_required
def receive_task():
	if request.method == 'POST':
		if current_user.is_authenticated:
			#获得POST来的task id
			json_data = json.loads(request.data)
			if 'tid' not in json_data:
				return json.dumps({'errmsg': '没有传递tid'})
			task = Task.query.filter_by(id=json_data['tid']).first()

			#如果没有这个任务则返回错误
			if task==None :
				return json.dumps({'errmsg': '没有该tid的任务'})
			print(len(task.receivers))

			#判断人数限制是否已经达到
			if task.receiver_limit <= len(task.receivers):
				print('receiver limit!')
				return json.dumps({'errmsg': '任务接收人数已满'})

			#判断是否重复接收任务
			for re in task.receivers:
				if re.uid == current_user.id:
					print('user had receivered this task!')
					return json.dumps({'errmsg': '用户已经接收了该任务'})

			#当满足条件，新建一个receiver
			# receiver = Receiver.query.filter_by(id=current_user.id).first()
			# if(receiver==None):
			receiver = Receiver(tid = json_data['tid'], uid = current_user.id)

			#接收任务
			task.receivers.append(receiver)
			task.received_number += 1
			print(task.receivers)

			db.session.add(receiver)
			db.session.commit()

			return json_true
	return json.dumps({'errmsg': '没有使用POST请求'})

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
		elif current_user.is_authenticated:
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
		elif current_user.is_authenticated:
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
	task_list = Task.query.order_by(-Task.received_number).all()
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
接收一个包含'tid'属性的json
返回对应task的详情
'''
@app.route('/search/task_id', methods=['GET', 'POST'])
def getTask_by_id():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'tid' in json_data:
            task = Task.query.filter_by(id=json_data['tid']).first()
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
            print('no tid')
            return json.dumps({'errmsg': '没有传递task_id'})

    return json.dumps({'errmsg': '没有使用POST请求'})


# 按id查询用户
'''
接收一个包含‘uid’属性的json
返回对应的用户详情的json
'''
@app.route('/search/user_id', methods=['GET', 'POST'])
def getUser_by_id():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'uid' in json_data:
            user = User.query.filter_by(id=json_data['uid']).first()
            if user==None:
                return json.dumps({'errmsg': '不存在该用户'})
            data = {'id':user.id, 'username':user.username, 'email':user.email, 'school':user.school,
                    'major':user.major, 'phone':user.phone, 'wx_number':user.wx_number, 'hobbit':user.hobbit, 'profile': user.profile}

            return json.dumps(data, sort_keys=False)
        return json.dumps({'errmsg': '没有传递uid'})
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
根据任务接收者uid和任务id查询问卷答案
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


'''
用户提交问卷答案 需要'user_id' 'task_id' 'answers'
'''
@app.route('/summit/answer', methods=['POST'])
def summit_answer():
	if request.method == 'POST':
		json_data = json.loads(request.data)
		if 'task_id' in json_data:
			if 'user_id' in json_data:
				if 'answers' in json_data:
					rec = Receiver.query.filter_by(uid=json_data['user_id'], tid=json_data['task_id']).first()
					if rec==None:
						return json.dumps({'errmsg': '没有这个任务或者该用户没有接受该任务'})
					rec.answers.answers = json_data['answers']
					db.session.commit()
					return json_true
			return json.dumps({'errmsg': '没有传递user_id'})
		return json.dumps({'errmsg': '没有传递task_id'})
	return json.dumps({'errmsg': '没有使用POST请求'})



'''
退出任务
接收 'user_id' 和 'task_id'
'''
@app.route('/task_quit', methods=['POST'])
def task_quit():
	if request.method == 'POST':
		json_data = json.loads(request.data)
		if 'task_id' in json_data:
			if 'user_id' in json_data:
				task = Task.query.filter_by(id=json_data['task_id']).first()
				rec = Receiver.query.filter_by(uid=json_data['user_id'], tid=json_data['task_id']).first()
				if (task==None or rec==None):
					return json.dumps({'errmsg': '用户id或任务id错误'})
				task.received_number -= 1
				for current_rec in task.receivers:
					if current_rec.uid == rec.uid:
						task.receivers.remove(current_rec)
						print('succeed')

				receiver = Receiver.query.filter_by(uid=json_data['user_id'], tid=json_data['task_id']).first()
				db.session.delete(receiver)
				db.session.commit()
				return json_true

			return json.dumps({'errmsg': '没有传递user_id'})
		return json.dumps({'errmsg': '没有传递task_id'})
	return json.dumps({'errmsg': '没有使用POST请求'})


'''
撤销任务
接收 'user_id' 和 'task_id'
'''
@app.route('/task_cancel', methods=['POST'])
def task_cancel():
	if request.method == 'POST':
		json_data = json.loads(request.data)
		if 'task_id' in json_data:
			if 'user_id' in json_data:
				task = Task.query.filter_by(id=json_data['task_id']).first()
				#判断task id是否正确
				if task==None:
					return json.dumps({'errmsg': '任务id错误，无该任务'})
				#判断是否是当前用户
				if task.sponsor.id != json_data['user_id']:
					return json.dumps({'errmsg': '该用户不是任务发起者'})

				receivers = Receiver.query.filter_by(tid=json_data['task_id']).all()
				for rec in receivers:
					db.session.delete(rec)
				task = Task.query.filter_by(id=json_data['task_id']).first()
				db.session.delete(task)
				db.session.commit()
				return json_true
			return json.dumps({'errmsg': '没有传递user_id'})
		return json.dumps({'errmsg': '没有传递task_id'})
	return json.dumps({'errmsg': '没有使用POST请求'})



'''
修改用户信息
'''
@app.route('/modify/user_info', methods=['POST'])
def modify_user_info():
	if request.method == 'POST':
		json_data = json.loads(request.data)
		if 'id' in json_data:
			user = User.query.filter_by(id=json_data['id']).first()
			print(user)
			if 'username' in json_data:
				user.username = json_data['username']
			if 'email' in json_data:
				user.email = json_data['email']
			if 'school' in json_data:
				user.school = json_data['school']
			if 'major' in json_data:
				user.major = json.date['major']
			if 'phone' in json_data:
				user.phone = json_data['phone']
			if 'wx_number' in json_data:
				user.wx_number = json_data['wx_number']
			if 'hobbit' in json_data:
				user.hobbit = json_data['hobbit']
			if 'profile' in json_data:
				user.profile = json_data['profile']
			db.session.commit()
			return json.dumps(user, default=UserToJson, sort_keys=False) 

		return json.dumps({'errmsg': '没有指定用户'})
	return json.dumps({'errmsg': '没有使用POST请求'})

# 测试
@app.route('/test', methods=['GET', 'POST'])
def test():
	#查询
	user = User.query.all()
	task = Task.query.all()
	receiver = Receiver.query.all()
	template = Template.query.all()
	answer = Answer.query.all()
	print('{}\n\n{}\n\n{}\n\n{}\n\n{}\n'.format(user,task,receiver,template,answer))
	print(task[0].sponsor.username)
	return json_true



