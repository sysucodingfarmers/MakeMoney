# -- coding:UTF-8 --
from app import app,db
from app.models import SingleChoice,MultipleChoice,EssayQuestion,Template,Answer
from app.models import User,Task,Receiver,receivers
import pdb

user1 = User(id =16340045, username = 'xiaotong', email = 'xiaotong@qq.com')
user1.set_password('xiaozhu')

user2 = User(id = 16340046, username = 'xiaohang', email = 'xiaohang@qq.com')
user2.set_password('xiaozhu2')

singechoice1 = SingleChoice(question = '单选题问题1',options = ['选项1', '选项2'])
singechoice2 = SingleChoice(question = '单选题问题2',options = ['选项1', '选项2','选项3'])

multiplechoice1 = MultipleChoice(question = '多选题问题1',options = ['选项1','选项2'])
multiplechoice2 = MultipleChoice(question = '多选题问题2',options = ['选项1','选项2','选项3'])

essayquestion1 = EssayQuestion(question = '问答题题目1')
essayquestion2 = EssayQuestion(question = '问答题题目2')

template1 = Template(\
	single_choices = [singechoice1,singechoice2],\
	multiple_choices = [multiplechoice1],\
	essay_questions = [])
template2 = Template(\
	single_choices = [],\
	multiple_choices = [multiplechoice2],\
	essay_questions = [essayquestion1,essayquestion2])


task1 = Task(
	id = 1,
	title = 'task1',
	sponsor = user1
	)
task2 = Task(
	id = 2,
	title = 'task2',
	sponsor = user2,
	template = template1,
	answers = [answer1, answer2]
	)


receiver1 = Receiver(uid=user1.id, tid=task1.id, finished = True)
receiver2 = Receiver(uid=user2.id, tid=task2.id, finished = True,paid = True)


answer1 = Answer(\
	receiver_id = receiver1.id,\
	answers = ['01', '100', '11'])
answer2 = Answer(\
	receiver_id = receiver2.id,\
	answers = ['101', '问答题1回答', '问答题2回答'])

db.session.add_all([user1,user2,task1,task2,receiver1,receiver2,template1,template2,answer1,answer2])
db.session.commit()

pdb.set_trace()
