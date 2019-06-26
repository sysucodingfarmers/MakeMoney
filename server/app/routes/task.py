# -- coding:UTF-8 --
from flask import render_template, redirect, url_for, request, json, send_from_directory
from flask_login import current_user,login_user,logout_user
from app import app,db
from app.models import Template,Answer, Session
from app.models import User,Task,Receiver,receivers
from app.utils.trans import UserToJson, TaskToJson
from datetime import datetime, timedelta
import os
import uuid
import cv2

json_true = json.dumps('succeed')
json_false = json.dumps('failed')
'''
发布任务（需登录）
接收新建任务的所有需求信息，以当前登录user进行发布
'''
@app.route('/task/sponsor', methods=['POST'])
def sponsor_task():
    #需要登录
    headers = request.headers
    se = Session.query.filter_by(sid = int(headers['session_id']), uid=int(headers['user_id'])).first()
    if se==None:
        print('session is not connected')
        return json.dumps({'errmsg': '没有建立会话或者会话信息出错'})
    user = User.query.filter_by(id=se.uid).first()
    login_user(user)

    if request.method == 'POST':
        #获得post来的task数据
        json_data = json.loads(request.data)
        print(json_data)

        if 'title' not in json_data or 'pay' not in json_data :
            return json.dumps({'errmsg': '没有传递title或者没有传递pay'})
        

        task = Task(
            title = json_data['title'],
            sponsor = current_user,
            type = json_data['type'] if 'type' in json_data else '问卷',
            start_time = datetime.strptime(json_data['start_time'],'%Y-%m-%dT%H:%M:%S.%fZ') if 'start_time' in json_data else datetime.now(),
            end_time = datetime.strptime(json_data['end_time'],'%Y-%m-%dT%H:%M:%S.%fZ') if 'end_time' in json_data else datetime.now()+timedelta(days=10),
            pay = json_data['pay'] if 'pay' in json_data else 0,
            detail = json_data['detail'] if 'detail' in json_data else None,
            receiver_limit = json_data['receiver_limit'] if 'receiver_limit' in json_data else 1,
            received_number = json_data['received_number'] if 'received_number' in json_data else 0,
            extra_content = json_data['extra_content'] if 'extra_content' in json_data else None,
            state = 0,
            # images = json_data['images'].encode() if 'images'in json_data else b''
            )
        #如果账户余额不足则返回错误
        paySum = task.pay * task.receiver_limit
        if paySum > current_user.exMoney:
            return json.dumps({'errmsg': '账户余额不足'})

        task.template = Template()
        task.template.questions = json_data['questions'] if 'questions' in json_data else []
        task.template.options = json_data['options'] if 'options' in json_data else []
        task.template.types = json_data['types'] if 'types' in json_data else []

        #任务发布成功，则提前扣除发布者的金额
        current_user.exMoney = current_user.exMoney - paySum
        current_user.expend = current_user.expend + paySum

        #提交
        db.session.add(task)
        db.session.commit()

        return json.dumps(task.id)

    return json.dumps({'errmsg': '没有使用POST请求'})

'''
接受任务(需登录）
接收任务的task_id，以当前user进行接收
'''
@app.route('/task/receive', methods=['POST'])
def receive_task():
    #需要登录
    headers = request.headers
    se = Session.query.filter_by(sid=int(headers['session_id']), uid=int(headers['user_id'])).first()
    if se==None:
        print('session is not connected')
        return json.dumps({'errmsg': '没有建立会话或者会话信息出错'})
    user = User.query.filter_by(id=se.uid).first()
    login_user(user)

    if request.method == 'POST':
        #获得POST来的task id
        json_data = json.loads(request.data)
        if 'task_id' not in json_data:
            return json.dumps({'errmsg': '没有传递task_id'})
        task = Task.query.filter_by(id=json_data['task_id']).first()

        #如果没有这个任务则返回错误
        if task==None :
            return json.dumps({'errmsg': '没有该task_id的任务'})
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
        receiver = Receiver(tid = json_data['task_id'], uid = current_user.id)

        #接收任务，修改任务状态
        task.receivers.append(receiver)
        task.received_number += 1
        if task.state == 0:
            task.state = 1
        print(task.receivers)

        db.session.add(receiver)
        db.session.commit()

        return json_true
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
                    rec.finished = True
                    task = Task.query.filter_by(id=json_data['task_id']).first()
                    task.finished_number = task.finished_number+1
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
                #如果任务已完成，无法退出
                if task.state == 2:
                    return json.dumps({'errmsg': '该任务已完成，无法退出'})
                if (task==None or rec==None):
                    return json.dumps({'errmsg': '用户id或任务id错误'})
                #如果已完成，则完成人数减一
                if rec.finished == True:
                    task.finished_number -= 1
                #接受人数减一并删除receiver
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


'''上传任务图片
接受任务的id
'''
@app.route('/task/postImage', methods=['POST'])
def postImage():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'task_id' in json_data:
            #查找任务
            task = Task.query.filter_by(id=json_data['task_id']).first()
            if task==None:
                return json.dumps({'errmsg': '任务id错误，无该任务'})
            filename = str(uuid.uuid1()) + ".jpg"
            task.images.append(filename)
            
            #取出数据
            f = request.files['image']
            user_input = request.form.get("task_id")
            #获得参数path和name
            path = os.path.join(app.config['TASK_FOLDER'])
            #存入服务器
            if os.path.exists(path)==False:
                os.makedirs(path)
            f.save(path + filename)
            #返回
            return send_from_directory(app.config['TASK_FOLDER'], filename)
        return json.dumps({'errmsg': '没有传递task_id'})
    return json.dumps({'errmsg': '没有使用POST请求'})


'''任务完成
接受者发出，接受user_id和task_id
返回True或False
'''
@app.route('/task/finished', methods=['POST'])
def taskFinished():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'user_id' in json_data and 'task_id' in json_data:
            #查找用户
            user = User.query.filter_by(id=json_data['user_id']).first()
            if user==None:
                return json.dumps({'errmsg': '用户id错误，无该用户'})
            #查找任务
            task = Task.query.filter_by(id=json_data['task_id']).first()
            if task==None:
                return json.dumps({'errmsg': '任务id错误，无该任务'})
            #查找接受者
            receiver = Receiver.query.filter_by(uid=json_data['user_id'], tid=json_data['task_id']).first()
            if receiver==None:
                return json.dump({'errmsg': '该用户无接受该任务'})
            #接受者完成
            receiver.finished = True
            #任务完成人数加一
            task.finished_number = task.finished_number + 1
            #用户收入以及零钱添加

            db.session.commit()
            return json_true
        return json.dumps({'errmsg': '没有传递user_id或没有task_id'})
    return json.dumps({'errmsg': '没有使用POST请求'})


'''支付
发起者发出，接受user_id和task_id
返回True或False
'''
@app.route('/task/pay', methods=['POST'])
def pay():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        if 'user_id' in json_data and 'task_id' in json_data:
            #查找用户
            user = User.query.filter_by(id=json_data['user_id']).first()
            if user==None:
                return json.dumps({'errmsg': '用户id错误，无该用户'})
            #查找任务
            task = Task.query.filter_by(id=json_data['task_id']).first()
            if task==None:
                return json.dumps({'errmsg': '任务id错误，无该任务'})
            #用户收钱
            pay = task.pay
            user.exMoney = user.exMoney + pay
            user.income = user.expend + pay
            task.paid_number = task.paid_number + 1

            db.session.commit()

            #如果任务已经全部支付，则修改任务的state
            if task.paid_number == task.receiver_limit:
                task.state = 2
                db.session.commit()
                return json.dumps({'msg': '任务已完成'})

            
            return json_true
        return json.dumps({'errmsg': '没有传递user_id或没有task_id'})
    return json.dumps({'errmsg': '没有使用POST请求'})

'''修改任务
传入要修改的信息
返回true or false
'''
