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
		hobit = json_data['hobit'] if 'hobit' in json_data else None
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
			db.session.add(task)
			db.session.commit()
			return json_true
	return json_true

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
				receiver = Receiver(id=1)
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
			print(task.receivers)
			db.session.commit()
			return json_true
	return json_true

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
		data = [{'task number':len(user.sponsor_tasks)}]
		i = 1
		for task in user.sponsor_tasks:
			# now = [{}]
			# now[0]['id'] = task.id
			print(task.id)
			now = json.dumps(task, default=TaskToJson)
			data[0][str(i)] = now
			i = i+1
		return json.dumps(data, sort_keys=False)
	return json_true

#查看接受的任务
@app.route('/task/myreceive', methods=['GET', 'POST'])
def my_receive_task():
	return json_true
# #根据用户爱好推荐
# @app.route('/recommend', methods=['POST'])
# def recommend():

# #查询
# @app.route('/require', methods=['POST'])
# def require():

#测试
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
