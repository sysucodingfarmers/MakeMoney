from app import app,db
from app.models import User, Task, Receiver

def UserToJson(user):
	return {
	    'id': user.id, 
	    'username': user.username, 
	    'email': user.email,
	    'school': user.school,
	    'major': user.major,
	    'phone': user.phone,
	    'wx_number': user.wx_number,
	    'hobbit': user.hobbit,
	    'profile': user.profile
	}

def TaskToJson(task):
	print(task)
	return {
		'id': task.id,
		'title': task.title,
		'type': task.type,
		# 'start_time': task.start_time, 
		# 'end_time': task.end_time,
		'pay': task.pay,
		'detail': task.detail,
		'receiver_limit': task.receiver_limit,
		'received_number': task.received_number,
		'extra_content': task.extra_content
	}