# -- coding:UTF-8 --
from flask import render_template, redirect, url_for, request, json
from flask_login import current_user,login_user,logout_user, login_required
from app import app,db
from app.models import SingleChoice,MultipleChoice,EssayQuestion,Template,Answer
from app.models import User,Task,Receiver,receivers
from app.trans import UserToJson, TaskToJson

json_true = json.dumps('succeed')
json_false = json.dumps('failed')
id_exist = json.dumps('id_exist')


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
			return json_false
	user = User(id = json_data['id'], 
		username = json_data['username'], 
		email = json_data['email'] if 'email' in json_data else None, 
		school = json_data['school'] if 'school' in json_data else None, 
		major = json_data['major'] if 'major' in json_data else None, 
		phone = json_data['phone'] if 'phone' in json_data else None, 
		wx_number = json_data['wx_number'] if 'wx_number' in json_data else None, 
		hobbit = json_data['hobbit'] if 'hobbit' in json_data else None
		)
	user.set_password(json_data['password'])
	db.session.add(user)
	db.session.commit()
	print('register user {}!'.format(user))
	return json_true

'''
登入:
接收账号密码
验证账户是否正确，正确则返回用户信息
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if current_user.is_authenticated:
			print('Error, user is active!')
			return json_false
		json_data = json.loads(request.data)
		# print(json_data)
		user = User.query.filter_by(id=json_data['id']).first()
		if user is None or not user.check_password(json_data['password']):
			print('username or password isn\'t correct!')
			return json_false
		login_user(user, remember=True)
		print('login user {}!'.format(user))
		return json.dumps(user, default=UserToJson) 
	return json_false

#登出
@app.route('/logout')
@login_required
def logout():
	logout_user()
	print('logout user succeed!')
	return json_true

'''
发布任务（需登录）:
接收新建任务的所有需求信息，以当前登录user进行发布
'''
@app.route('/task/sponsor', methods=['GET', 'POST'])
@login_required
def sponsor_task():
	if request.method == 'POST':
		if current_user.is_authenticated:
			#获得post来的task数据
			json_data = json.loads(request.data)
			if (Task.query.filter_by(id=json_data['id']).first() != None):
				print('existed')
				return json_false
			else:
				task = Task(id = json_data['id'],
					title = json_data['title'],
					sponsor = current_user,
					type = json_data['type'] if 'type' in json_data else 'query', 
				# start_time = json_data['start_time'] if 'start_time' in json_data else None, 
				# end_time = json_data['end_time'] if 'end_time' in json_data else None, 
					pay = json_data['pay'] if 'pay' in json_data else 0, 
					detail = json_data['detail'] if 'detail' in json_data else None, 
					receiver_limit = json_data['receiver_limit'] if 'receiver_limit' in json_data else 1, 
					received_number = json_data['received_number'] if 'received_number' in json_data else 0, 
					extra_content = json_data['extra_content'] if 'extra_content' in json_data else None, 
					)

				task.template.single_choices.question = json_data['single_choices_question']
				task.template.single_choices.options = json_data['single_choices_options']
				task.template.multiple_choices.question = json_data['multiple_choices_question']
				task.template.multiple_choices.options = json_data['multiple_choices_options']
				task.template.essay.quetion = json_data['essay_question']

				db.session.add(task)
				db.session.commit()
				return json_true
	return json_false

'''
接受任务(需登录）:
接收任务的id，以当前user进行接收
'''
@app.route('/task/receiver', methods=['POST'])
@login_required
def receive_task():
	if request.method == 'POST':
		if current_user.is_authenticated:
			#获得POST来的task id
			json_data = json.loads(request.data)
			task = Task.query.filter_by(id=json_data['id']).first()
			# print(task)
			receiver = Receiver.query.filter_by(id=current_user.id).first()
			if(receiver==None):
				receiver = Receiver(json_data['id'], current_user.id)
			print(len(task.receivers))
			#判断人数限制是否已经达到
			if task.receiver_limit <= len(task.receivers):
				print('receiver limit!')
				return json_false
			#判断是否重复接收任务
			for re in task.receivers:
				if re.id == current_user.id:
					print('user had receivered this task!')
					return json_false
			#接收任务
			task.receivers.append(receiver)
			task.received_number += 1
			print(task.receivers)
			db.session.add(receiver)
			db.session.commit()
			return json_true
	return json_false

'''
查看发布的任务（无需登录）返回task id:
如果有post一个user的id，则查询该id发布的任务,
若无post一个id则查询登录的user的任务
如果无id且无登录，则返回false
'''
@app.route('/task/mysponsor', methods=['GET', 'POST'])
def my_sponsor_task():
	if request.method == 'POST':
		json_data = json.loads(request.data)
		if 'id' in json_data:
			user = User.query.filter_by(id=json_data['id']).first()
		elif current_user.is_authenticated:
			user = current_user
		else:
			print('query error!')
			return json_false
		#返回
		data = [{'task_number':len(user.sponsor_tasks)}]
		i = 1
		for task in user.sponsor_tasks:
			# now = [{}]
			# now[0]['id'] = task.id
			print(task.id)
			now = json.dumps(task, default=TaskToJson)
			data[0][str(i)] = now
			i = i+1
		return json.dumps(data[0] , sort_keys=False)
	return json_false

# 查看接受的任务


@app.route('/task/myreceive', methods=['GET', 'POST'])
def my_receive_task():
	if request.method == 'POST':
		json_data = json.loads(request.data)
		if 'id' in json_data:
			receiver = Receiver.query.filter_by(id=json_data['id']).all()
		#返回
		data = {'task_number': len(receiver), 'task_id': []}
		for rec in receiver:
			data['task_id'].append(rec.tid);
		return json.dumps(data, sort_keys=False)
	return json_false





# 任务广场的推荐
@app.route('/recommend', methods=['POST'])
def recommend():
	if request.method == 'POST':
		task_list = Task.query.order_by(-Task.received_number).all()
		data = {"task_number":len(task_list), "task_id": []}
		for task in task_list:
			data['task_id'].append(task.id)
		return json.dumps(data, sort_keys=False)
	return json_false


# #查询
# @app.route('/require', methods=['POST'])
# def require():


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
			task_list = Task.query.filter_by(sponsor=json_data['sponsor'])
		else:
			print('no match result')
			return json_false

		#正确查询之后返回json
		data = {'task_number':len(task_list), 'task_id':[]}
		for task in task_list:
			data['task_id'].append(task.id)
		return json.dumps(data, sort_keys=False)

	return json_false

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
            task_list = Task.query.filter_by(Task.title.like(key))
        else:
            print('no match result')
            return json_false

        #正确查询之后返回json
        data = {'task_number':len(task_list), 'task_id':[]}
        for task in task_list:
            data['task_id'].append(task.id)
        return json.dumps(data, sort_keys=False)

    return json_false


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
            task_list = Task.query.filter_by(Task.detail.like(key))
        else:
            print('no match result')
            return json_false

        # 正确查询之后返回json
        data = {'task_number':len(task_list), 'task_id':[]}
        for task in task_list:
            data['task_id'].append(task.id)
        return json.dumps(data, sort_keys=False)

    return json_false


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
            data = {'id':task.id, 'title':task.title, 'type':task.type,
                    'start_time':task.start_time, 'end_time':task.end_time,
                    'pay':task.pay, 'detail':task.detail, 'receiver_limit':task.receiver_limit,
                    'received_number':task.received_number, 'finished_number':task.finished_number,
                    'extra_content':task.extra_content, 'sponsor_id':task.sponsor.id,
                    'sponsor':task.sponsor.name, 'template_id':task.template.id}
            receivers_id = []
            for rec in task.receivers:
                receivers_id.append(rec.id)
            data['receivers'] = receivers_id
            return json.dumps(data, sort_keys=False)

        else:
            print('no task_id')
            return json_false

    return json_false


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
            data = {'id':user.id, 'username':user.username, 'email':user.email, 'school':user.school,
                    'major':user.major, 'phone':user.phone, 'wx_number':user.wx_number, 'hobbit':user.hobbit}

            return json.dumps(data, sort_keys=False)
        return json_false
    return json_false


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
			data = {'id': template.id,
					'single_choices_question': template.single_choices.question,
					'single_choices_options': template.single_choices.options,
					'multiple_choices_question': template.multiple_choices.question,
					'multiple_choices_options': template.multiple_choices.options,
					'essay_question': template.essay_questions.question
					}

			return json.dumps(data, sort_keys=False)
		return json_false
	return json_false


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
				ans = rec.answers.answers

				data = {'single_choices_options': ans['single_choices_options'],
						'multiple_choices_options': ans['multiple_choices_options'],
						'essay_answer': ans['essay_answer']}
				return json.dumps(data, sort_keys=False)

			return json_false
		return json_false
	return json_false


'''
用户提交问卷答案 需要提'user_id' 'task_id'
'''

@app.route('/summit/answer')
def summit_answer():
	if request.method == 'POST':
		json_data = json.loads(request.data)
		if 'task_id' in json_data:
			if 'user_id' in json_data:
				rec = Receiver.query.filter_by(uid=json_data['user_id'], tid=json_data['task_id']).first()

				rec.answers.answers = {'single_choices_options': json_data['single_choices_options'],
					   'multiple_choices_options': json_data['multiple_choices_options'],
					   'essay_answer': json_data['essay_answer']
					   }
				return json_true

			return json_false
		return json_false
	return json_false



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

				task.received_number -= 1
				for current_rec in task.receivers:
					if current_rec.uid == rec.uid:
						task.receivers.remove(current_rec)

				Receiver.query.filter_by(uid=json_data['user_id'], tid=json_data['task_id']).first().delete()

				db.commit()
				return json_true

			return json_false
		return json_false
	return json_false


'''
撤销任务
接收 'user_id' 和 'task_id'
'''
@app.route('/task_quit', methods=['POST'])
def task_quit():
	if request.method == 'POST':
		json_data = json.loads(request.data)
		if 'task_id' in json_data:
			if 'user_id' in json_data:
				task = Task.query.filter_by(id=json_data['task_id']).first()
				if task.sponsor.id != json_data['user_id']:
					return json_false

				Receiver.query.filter_by(tid=json_data['task_id']).all().delete()

				Task.query.filter_by(id=json_data['task_id']).first().delete()

				db.commit()
				return json_true

			return json_false
		return json_false
	return json_false

# 测试
@app.route('/test', methods=['POST'])
def test():
	#查询
	user = User.query.all()
	task = Task.query.all()
	receiver = Receiver.query.all()
	template = Template.query.all()
	answer = Answer.query.all()
	print('{}\n\n{}\n\n{}\n\n{}\n\n{}\n'.format(user,task,receiver,template,answer))
	
	#修改数据
	# user.username = 'xiaotong'
	# user.set_password('xiaozhu')
	# db.session.commit()
	
	#删除数据
	# result = Article.query.filter(Article.title == 'aaa').first()
	# db.session.delete(result)
	# db.session.commit()

	return json_true


