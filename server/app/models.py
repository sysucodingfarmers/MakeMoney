from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
#用户验证用户是否登录，加入到User的继承中
from flask_login import UserMixin
from datetime import datetime, timedelta

#User和Task之间的多对多关系
receivers = db.Table('receivers',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(UserMixin, db.Model):
	#初始化方法，或者在routes.py 中email = json_data['email'] if 'email' in json_data else None
	def __init__(self, **kwargs):
		if 'email' not in kwargs:
			kwargs['email'] = self.__table__.c.email.default.arg
		super(User, self).__init__(**kwargs)
	#学号(账号)
	id = db.Column(db.Integer, primary_key=True)
	#用户名
	username = db.Column(db.String(20), nullable=False)
	#密码hash
	password_hash = db.Column(db.String(128))
	#邮箱
	email = db.Column(db.String(20), default='.com')
	#学院及专业
	school = db.Column(db.String(20))
	major = db.Column(db.String(20))
	#手机号
	phone = db.Column(db.Integer)
	#微信号
	wx_number = db.Column(db.Integer)
	#兴趣爱好
	hobit = db.Column(db.String(20))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	def __repr__(self):
		return '<User {} {}>'.format(self.id, self.username)


class Receiver(User):
	'''
	只提供 继承User 一种初始化方法，如
	receiver = Receiver(user, finished=True, paid=False)
	'''
	def __init__(self, User, **kwargs):
		super(Receiver, self).__init__(
			id = User.id,
			username = User.username,
			password_hash = User.password_hash,
			email = User.email,
			school = User.school,
			major = User.major,
			phone = User.phone,
			wx_number = User.wx_number,
			hobit = User.hobit)
		# print(kwargs['finished'])
		self.finished = self.__table__.c.finished.default.arg if 'finished' not in kwargs else kwargs['finished']
		self.paid = self.__table__.c.paid.default.arg if 'paid' not in kwargs else kwargs['paid']

	finished = db.Column(db.Boolean, default=False)
	paid = db.Column(db.Boolean, default=False)
	def __repr__(self):
		return '<Receiver {} {} {} {}>'.format(self.id, self.username, self.finished, self.paid)

class Task(db.Model):
	#初始化
	def __init__(self, **kwargs):
		if 'start_time' not in kwargs:
			kwargs['start_time'] = self.__table__.c.start_time.default.arg
		if 'end_time' not in kwargs:
			kwargs['end_time'] = self.__table__.c.end_time.default.arg
		if 'type' not in kwargs:
			kwargs['type'] = self.__table__.c.type.default.arg
		if 'receiver_limit' not in kwargs:
			kwargs['receiver_limit'] = self.__table__.c.receiver_limit.default.arg
		if 'finished_number' not in kwargs:
			kwargs['finished_number'] = self.__table__.c.finished_number.default.arg
		super(Task, self).__init__(**kwargs)
	#任务id
	id = db.Column(db.Integer, primary_key=True)
	#题目
	title = db.Column(db.String(20), nullable=False)
	#任务类型
	type = db.Column(db.String(20), default='query')
	#时间，默认结束时间为10天后
	start_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
	end_time = db.Column(db.DateTime, nullable=False, default=datetime.now()+timedelta(days=10))
	#报酬
	pay = db.Column(db.Integer, nullable=False)
	#任务详情
	detail = db.Column(db.Text)
	#任务人数上限
	receiver_limit = db.Column(db.Integer, nullable=False, default=1)
	#目前完成人数
	finished_number = db.Column(db.Integer, nullable=False, default=0)
	#额外内容
	extra_content = db.Column(db.Text)

	#任务发起者
	sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	sponsor = db.relationship('User', backref=db.backref('sponsor_tasks', lazy=True))
	
	#任务接受者
	receivers = db.relationship('Receiver', secondary=receivers, lazy='subquery',
		backref=db.backref('receive_tasks', lazy=True))

	def __repr__(self):
		return '<Task {} {}>'.format(self.id, self.title)


#login的配置，使login生效
@login.user_loader
def load_user(id):
	return User.query.get(int(id))