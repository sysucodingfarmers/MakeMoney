from flask import render_template, redirect, url_for, request, json
from flask_login import current_user,login_user,logout_user, login_required
from app import app,db
from app.models import User

json_true = json.dumps('succeed')
json_false = json.dumps('failed')


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

#接受账号密码，验证格式，验证重复，存入数据库
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return json_false
	json_data = json.loads(request.data)
	print(json_data['id'])
	user = User(id = json_data['id'], \
		username = json_data['username'], \
		)
	user.set_password(json_data['password'])
	db.session.add(user)
	db.session.commit()
	return json_true

#登入，验证账号密码正确，返回用户信息
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if current_user.is_authenticated:
			return json_false
		json_data = json.loads(request.data)
		# print(json_data)
		user = User.query.filter_by(id=json_data['id']).first()
		if user is None or not user.check_password(json_data['password']):
			return json_false
		login_user(user, remember=True)
		return json_true
	return json_false
#登出
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return json_true

# #用户id的发布任务
# @app.route('/publish_task', methods=['POST'])
# def publish_task():

# #用户id的接受任务
# @app.route('/receive_task', methods=['POST'])
# def receive_task():

# #根据用户爱好推荐
# @app.route('/recommend', methods=['POST'])
# def recommend():

# #查询
# @app.route('/require', methods=['POST'])
# def require():

#测试
# @app.route('/test', methods=['POST'])
# def test():
# 	data = request.data
# 	json_data = json.loads(data)
# 	print(data)
# 	print(json_data)
# 	r_json = json.dumps({'key1': 'value1', 'key2': 'value2'})
# 	return r_json