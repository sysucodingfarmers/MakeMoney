from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
#用户验证用户是否登录，加入到User的继承中
from flask_login import UserMixin
from datetime import datetime, timedelta

class User(UserMixin, db.Model):
	#学号(账号)
	id = db.Column(db.Integer, primary_key=True)
	#用户名
	username = db.Column(db.String(20), nullable=False)
	#密码hash
	password_hash = db.Column(db.String(128))
	#邮箱
	email = db.Column(db.String(20), nullable=True)
	#学院及专业
	school = db.Column(db.String(20))
	major = db.Column(db.String(20))
	#手机号
	phone = db.Column(db.Integer)
	#微信号
	wx_number = db.Column(db.Integer, nullable=False)
	#兴趣爱好
	hobit = db.Column(db.String(20))

	#与任务的联系
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
	tasks = db.relationship('Task', backref=db.backref('author', lazy=True) )
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	def __repr__(self):
		return '<User {} {} {}>'.format(self.id, self.username, self.task_id)

class Task(db.Model):
	#任务id
	id = db.Column(db.Integer, primary_key=True)
	#题目
	title = db.Column(db.String(20))
	#任务类型
	type = db.Column(db.String(20))
	#时间，默认结束时间为5天后
	strat_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
	end_time = db.Column(db.DateTime, nullable=False, default=datetime.now()+timedelta(days=5))
	#报酬
	pay = 
	#任务详情
	detail = db.Column(db.Text)
	#接受者
	receiver = 
		#是否完成
		finished = 
		#是否支付
		paid = 
	#任务人数上限
	receiver_limit = 
	#目前完成人数
	finished_number = 
	#额外内容
	extra_content = 

	def __repr__(self):
		return '<Task {} {}>'.format(self.id, self.title)

#login的配置，使login生效
@login.user_loader
def load_user(id):
	return User.query.get(int(id))