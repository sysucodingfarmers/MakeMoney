# -- coding:UTF-8 --
from flask import render_template, redirect, url_for, request, json
from flask_login import current_user,login_user,logout_user, login_required
from app import app,db
from app.models import Template,Answer
from app.models import User,Task,Receiver,receivers
from app.utils.trans import UserToJson, TaskToJson

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
	print(json_data)
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
		if current_user.is_active:
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

	return json_true



