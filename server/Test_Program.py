#-*- coding:utf-8 -*-
import json
import requests
import pdb

url = 'http://localhost:5050'
# -- coding:UTF-8 --
url_register = url+'/register'
url_login = url+'/login'
url_logout = url+'/logout'
url_sponsor_task = url+'/task/sponsor'
url_receive_task = url+'/task/receive'
url_test = url+'/test'
url_mysponsor_tasks = url+'/task/mysponsor'
url_myreceive_tasks = url+'/task/myreceive'
url_recommend = url+'/recommend'

s = requests.Session()

# 测试，输出数据库的表
s.get(url_test)

#register
data1 = json.dumps({'id':12344321, 'password':'password', 'username':'Jack'})
res1 = s.post(url_register, data1)
print(json.loads(res1.text))

data2 = json.dumps({'id':12344321, 'password':'password', 'username':'Jack'})
res2 = s.post(url_register, data2)
print(json.loads(res2.text))

#login
#账号密码 错误
data3 = json.dumps({'id':12, 'password':'error'})
res3 = s.post(url_login, data3)
print(json.loads(res3.text))
#账号密码正确
data4 = json.dumps({'id':12344321, 'password':'password'})
res4 = s.post(url_login, data4)
print(json.loads(res4.text))

#发布任务
data5 = json.dumps({'title':'mykeymy',
 'type':'query',
 'pay':15, 
 'detail':'detail', 
 'receiver_limit':5, 
 'extra_content':'extra_content',
 'questions': ['q1','q2'],
 'options':[['q1 o1','q1 o2'], ''],
 'types':[1,3]
})
res5 = s.post(url_sponsor_task, data5)
print(json.loads(res5.text))

#查询我的发布任务
res = s.post(url_mysponsor_tasks ,json.dumps({'id': 12344321}))
print(json.loads(res.text))

#换一个用户，测试接受任务
s.get(url_logout)
#注册
data1 = json.dumps({'id':12344322, 'password':'password', 'username':'Mike'})
res1 = s.post(url_register, data1)
#登录
data4 = json.dumps({'id':12344322, 'password':'password'})
res4 = s.post(url_login, data4)
print(json.loads(res4.text))
#接受任务
data = json.dumps({'tid':2})
res = s.post(url_receive_task, data)
print(json.loads(res.text))

#查询我的接受任务
res = s.post(url_myreceive_tasks, json.dumps({'id': 12344322}))
print(json.loads(res.text))
print(1)
#测试推荐广场
res = s.post(url_recommend, json.dumps({}))
print(json.loads(res.text))

# 测试/search/sponsor
urlnow = url+'/search/sponsor'
res = s.post(urlnow, json.dumps({'sponsor': 'Jack'}))
print(json.loads(res.text))

#测试/search/title_key_word 和 /search/detail_key_word
urlnow = url+'/search/title_key_word'
res = s.post(urlnow, json.dumps({'key_word': 'key'}))
print(json.loads(res.text))

urlnow = url+'/search/detail_key_word'
res = s.post(urlnow, json.dumps({'key_word': 'de'}))
print(json.loads(res.text))

#测试/search/task_id，id返回任务详情
urlnow = url+'/search/task_id'
res = s.post(urlnow, json.dumps({'tid':2}))
print(json.loads(res.text))

#测试/search/user_id，id返回用户详情
urlnow = url+'/search/user_id'
res = s.post(urlnow, json.dumps({'uid':12344321}))
print(json.loads(res.text))

#测试/search/template_id，id返回模板详情
urlnow = url+'/search/template_id'
res = s.post(urlnow, json.dumps({'template_id': 1}))
print(json.loads(res.text))

#测试/search/answer，根据任务接收者uid和任务id查询问卷答案
urlnow = url+'/search/answer'
res = s.post(urlnow, json.dumps({'task_id':1, 'user_id':1234321}))
print(json.loads(res.text))

#测试/summit/answer
urlnow = url+'/summit/answer'
res = s.post(urlnow, json.dumps({'task_id':2, 'user_id':12344322, 'answers': ['01', '011', '我觉得']}))
print(json.loads(res.text))

#测试/task_quit
urlnow = url+'/task_quit'
res = s.post(urlnow, json.dumps({'task_id': 2, 'user_id': 12344322}))
print(json.loads(res.text))

#测试/task_cancel
urlnow = url+'/task_cancel'
res = s.post(urlnow, json.dumps({'task_id': 2, 'user_id': 12344321}))
print(json.loads(res.text))

#测试/modify/user_info
urlnow = url+'/modify/user_info'
res = s.post(urlnow, json.dumps({'id':12344321, 'wx_number': 'I am wx_number2', 'email': 'I am email'}))
print(json.loads(res.text))

# pdb.set_trace()
