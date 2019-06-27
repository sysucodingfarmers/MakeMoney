### API调用文档

-----
```python
我们约定
json_true = json.dumps('succeed')
json_false = json.dumps('failed')
```
-----

- 注册API 

- 地址：'/register' 

- 接受POST请求

- 接收的json格式应包含

    - {‘id’: 

      'username':

      'email':

      'school':

      'major':

      'phone':

      'wx_number':

      'hobbit':

      'profile': }

      'profile'为用户头像照片的base64编码后的字符串

- 注册成功返回json_true, 失败则返回包含‘errmsg’的json文件

----

登陆API 

- 地址：'/login' 
- 接受POST请求
- 接收的json格式应包含
  - {‘id’: 
    'password':}

- 登陆成功返回json_true, 失败则返回包含‘errmsg’的json文件
  
-----
登出API 

- POST或者GET

- 地址：'/logout' 
- 成功登出返回json_true
  
  
-----
发布任务API 

- 地址：'/task/sponsor' 
- 接受POST请求，要求用户先登录才能发布
- 接收的json格式应包含
  - {
    'title':
    'type':
    'pay':
    'detail':
    'receiver_limit':
    'received_number':
    'extra_content':
    'questions': []
    'options': [[], [], .. []]
    'types': []
    }
  - questions是一个存储问题的list，比如 ['abc', 'dd']
  - options是一个存储选项的list,每个元素也是一个list，存储对应问题的选项，如果对应问是个问答题，则，则对应的元素是一个空list，比如 [ ['a', 'b', 'c'],  ['a', 'b'] , [] ] （第三题是问答题）
  - types是一个list，用记录对应问题是单选/多选/问答
- 注册成功返回json_true, 失败则返回包含‘errmsg’的json文件

-----
接收任务API 

- 地址：'/task/receive' 
- 接受POST请求，要求用户先登录才能接收任务
- 接收的json格式应包含

  - {‘id’: 任务的id}

- 注册成功返回json_true, 失败则返回包含‘errmsg’的json文件
  
  
-----
查看发布的任务API 

- 地址：'/task/mysponsor' 
- 接受POST请求，若json中包含'id‘则查询改id用户的发布的任务，若无’id‘属性，则查询当前登陆用户的发布任务'
- 接收的json格式应包含
  - {‘id’: 用户的id}

- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
  				'task_id':[]}
-----
查看接收的任务API 

- 接受POST请求，要求用户先登录才能查看，可以传入查询的用户id，如果没有传入，则查询当前用户的接受任务

- 地址：'/task/myreceive‘' 
- 接受POST请求，若json中包含'id‘则查询改id用户的发布的任务
- 接收的json格式应包含
  - {‘id’: 用户的id}

- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
根据发布者的用户名搜索任务API 

- 地址：'/search/sponsor’ 
- 接受POST请求
- 接收的json格式应包含
  - {‘sponsor’: 要查询的发起者的username}

- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
根据任务标题进行模糊搜获API 

- 地址：'/search/title_key_word’ 
- 接受POST请求
- 接收的json格式应包含
  - {‘key_word’: 要查询的关键字}

- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
推荐任务API 

- 地址：'/recommend’ 
- POST或GET
- 失败返回包含‘errmsg’的json文件
- 成功返回如下json：{'task_number':
  				'task_info':[ {‘id’:  'title':   'detal':    'type':   }, {‘id’:  'title':   'detal':    'type':   } , ... ]}
- 备注：这个API事实上返回了所有发布中的任务，推荐顺序跟task_id中的排序一致

-----
根据任务详情进行模糊搜获API 

- 地址：'/search/detail_key_word’ 
- 接受POST请求
- 接收的json格式应包含
  - {‘key_word’: 要查询的关键字}

- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----

根据id获得任务详情API 

- 地址：'/search/task_id’ 

- 接受POST请求

- 接收的json格式应包含

  - {‘task_id’: 任务的id}

- 查询失败返回包含‘errmsg’的json文件

- 查询成功返回如下json：{'id':

   ​					"title":
   ​					'type':

   ​					'start_time':

   ​					'end_time':

   ​					'pay':

   ​					'detail':

   ​					'receiver_limit':

   ​					'received_number':

   ​					'finished_number'::

   ​					'extra_content':

   ​					'sponsor_id':

   ​					'sponsor':

   ​					'template_id':

   ​					}

   
-----
根据id获得用户详情API 

- 地址：'/search/user_id’ 

- 接受POST请求

- 接收的json格式应包含

  - {‘user_id’: 任务的id}

- 查询失败返回包含‘errmsg’的json文件

- 查询成功返回如下json：{'id':

  ​					"username":
  ​					'email':

  ​					'school':

  ​					'major':

  ​					'phone':

  ​					'wx_number':

  ​					'hobbit':

  ​					‘profile’：

  ​					}

----

根据id获得问卷模板API
- 地址: '/search/template_id'
- 接收POST请求
- 接收的json格式应包含 ‘templa_id’属性
- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json
- {
    'id': template_id,
    'questions':[],
    'options':[[],[],...,[]],
    'types':[]
    }

-----
用户提交问卷答案API
- 地址: '/summit/answer'
- 接收POST请求
- 接收的json如下
  {
    'user_id': 任务接收者的user id，
    'task_id': 接收的任务的task id
    'answers':[]，
  }
- ‘answers’中的每一个元素表示对应问题的答案
- 成功提交返回json_true，失败返回包含‘errmsg’的json文件

----
根据任务接收者uid和任务id查询问卷答案API
- 地址：‘/search/answer’
- 接收POST请求
- 接收如下josn
{
  ‘user_id’: 
  'task_id':
}
- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回json
  -{
    'answers':[]
  }

---
退出任务API
- 地址:'/task_quit'
- 接收POST请求
- 接收如下json
{
    'user_id':
    'task_id':
}
- 退出成功返回json_true，失败返回包含‘errmsg’的json文件

---
取消任务API
- 地址: '/task_cancel'
- 接收POST请求
- 接收如下json
{
    'user_id':
    'task_id':
}
- 退出成功返回json_true, 失败返回包含‘errmsg’的json文件

-----

修改用户信息API

- 地址‘/modify/user_info’

- 接收POST请求

- 接收的json必须包含‘id’信息，可包含以下信息
  - ‘username’
  - ‘email’
  - ‘school’
  - ‘major’
  - ‘phone’
  - ‘wx_number’
  - ‘hobbit’
  - 'profile'

- 修改成功返回user信息json（与查询user信息APIi一致），失败返回包含‘errmsg’的json
