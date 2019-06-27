# -- coding:UTF-8 --
from flask import render_template, redirect, url_for, request, json, make_response
from flask_login import current_user,login_user,logout_user
from app import app,db
from app.models import Template,Answer,Session
from app.models import User,Task,Receiver,receivers
from app.utils.trans import UserToJson, TaskToJson
from app.utils.email_code import send_email_code

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
        hobbit = json_data['hobbit'] if 'hobbit' in json_data else None
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
        #获取post来的数据
        json_data = json.loads(request.data)
        user = User.query.filter_by(id=json_data['id']).first()
        if user is None or not user.check_password(json_data['password']):
            print('username or password isn\'t correct!')
            return json.dumps({'errmsg': '用户名或密码错误'})
        login_user(user)
        
        #建立session数据库
        se = Session.query.filter_by(uid=user.id).first()
        if se==None:
            se = Session(uid=user.id)
            db.session.add(se)
            db.session.commit()
            print('Create a new session {}'.format(se.sid))
        else:
            print('Resume Session {}'.format(se.sid))

        print('login user {}!'.format(user))
        data = json.dumps(user, default=UserToJson, sort_keys=False) 
        
        #生成返回的resp，增加session的选项
        resp = make_response()
        resp.headers['session_id'] = str(se.sid)
        resp.data = data
        return resp
    return json.dumps({'errmsg': '没有使用POST请求'})

#登出
@app.route('/logout', methods=['POST'])
def logout():
    headers = request.headers
    se = Session.query.filter_by(sid=int(headers['session_id']), uid=int(headers['user_id'])).first()
    if se==None:
        print('session is not connected')
        return json.dumps({'errmsg': '没有建立会话或者会话信息出错'})
    
    #删除session
    db.session.delete(se)
    db.session.commit()
    #登出
    logout_user()
    print('logout user succeed!')
    return json_true

'''
修改用户信息，需要登录
'''
@app.route('/modify/user_info', methods=['POST'])
def modify_user_info():
    headers = request.headers
    se = Session.query.filter_by(sid=int(headers['session_id']), uid=int(headers['user_id'])).first()
    if se==None:
        print('session is not connected')
        return json.dumps({'errmsg': '没有建立会话或者会话信息出错'})
    
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

'''上传头像
接受用户的id
'''
@app.route('/postProfile', methods=['POST'])
def postProfile():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'user_id' in json_data:
            #查找用户
            user = User.query.filter_by(id=json_data['user_id']).first()
            if user==None:
                return json.dumps({'errmsg': '用户id错误，无该用户'})
            filename = str(uuid.uuid1()) + ".jpg"
            user.profile = filename
            
            #取出数据
            f = request.files['image']
            user_input = request.form.get("task_id")
            #获得参数path和name
            path = os.path.join(app.config['PROFILE_FOLDER'])
            #存入服务器
            if os.path.exists(path)==False:
                os.makedirs(path)
            f.save(path + filename)
            #返回
            return send_from_directory(app.config['PROFILE_FOLDER'], filename)
        return json.dumps({'errmsg': '没有传递user_id'})
    return json.dumps({'errmsg': '没有使用POST请求'})


'''查看钱包状态
传入user_id
返回钱包的余额，收入和支出
'''
@app.route('/wallet', methods=['POST'])
def wallet():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'user_id' in json_data:
            #查找用户
            user = User.query.filter_by(id=json_data['user_id']).first()
            if user==None:
                return json.dumps({'errmsg': '用户id错误，无该用户'})
            return json.dumps({'exMoney': user.exMoney, 'income': user.income, 'expend': user.expend})
        return json.dumps({'errmsg': '没有传递user_id'})
    return json.dumps({'errmsg': '没有使用POST请求'})

'''充值
传入user_id和value
返回账户金额
'''
@app.route('/recharge', methods=['POST'])
def recharge():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'user_id' in json_data and 'value' in json_data:
            #查找用户
            user = User.query.filter_by(id=json_data['user_id']).first()
            if user==None:
                return json.dumps({'errmsg': '用户id错误，无该用户'})
            print(user.exMoney)
            user.exMoney = user.exMoney + json_data['value']
            db.session.commit()
            print(user.exMoney)
            return json.dumps({'exMoney': user.exMoney})
        return json.dumps({'errmsg': '没有传递user_id或没有传递充值金额value'})
    return json.dumps({'errmsg': '没有使用POST请求'})

'''提现
传入user_id和value
返回账户金额
'''
@app.route('/withdraw', methods=['POST'])
def withdraw():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'user_id' in json_data and 'value' in json_data:
            #查找用户
            user = User.query.filter_by(id=json_data['user_id']).first()
            if user==None:
                return json.dumps({'errmsg': '用户id错误，无该用户'})
            print(user.exMoney)
            if user.exMoney - json_data['value'] < 0:
                return json.dumps({'errmsg': '账户余额不足'})
            user.exMoney = user.exMoney - json_data['value']
            db.session.commit()
            print(user.exMoney)
            return json.dumps({'exMoney': user.exMoney})
        return json.dumps({'errmsg': '没有传递user_id或没有传递充值金额value'})
    return json.dumps({'errmsg': '没有使用POST请求'})

#验证邮箱
@app.route('/sendemailcode', methods=['POST'])
def sendemailcode():
	if (request.method == 'POST'):
		json_data = json.load(request.data)
		print(json_data)
		if 'code' in json_data and 'target_email' in json_data:
			code = json_data['code']
			target_email = json_data['target_email']
			if (send_email_code(code, target_email)):
				return json_true
			else:
				return json.dump({'errmsg': '发送错误，请检查邮箱是否正确'})
		return json.dump({'errmsg': '没有验证码或邮箱地址'})
	return json.dump({'errmsg': '没有使用POST请求'})



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
	print(1)
	return json_true



