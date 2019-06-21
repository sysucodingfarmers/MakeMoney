### API调用文档

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

      'hobbit':}

- 注册成功返回json_true, 失败则返回json_false

----

登陆API 

- 地址：'/login' 
- 接受POST请求
- 接收的json格式应包含
  - {‘id’: 
    'password':}

- 登陆成功返回json_true, 失败则返回json_false
  
-----
登出API 

- 地址：'/logout' 
- 成功登出返回json_true
  
  
-----
发布任务API 

- 地址：'/task/sponsor' 
- 接受POST请求，要求用户先登录才能发布
- 接收的json格式应包含
  - {‘id’: 任务的id
    'title':
    'type':
    'pay':
    'detail':
    'receiver_limit':
    'received_number':
    'extra_content':}
- 注册成功返回json_true, 失败则返回json_false


-----
接收任务API 

- 地址：'/task/recevier' 
- 接受POST请求，要求用户先登录才能接收任务
- 接收的json格式应包含

  - {‘id’: 任务的id}

- 注册成功返回json_true, 失败则返回json_false
  
  
-----
查看发布的任务API 

- 地址：'/task/mysponsor' 
- 接受POST请求，若json中包含'id‘则查询改id用户的发布的任务，若无’id‘属性，则查询当前登陆用户的发布任务'
- 接收的json格式应包含
  - {‘id’: 用户的id}

- 查询失败返回json_false
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
  
-----
查看接收的任务API 

- 地址：'/task/myreceive‘' 
- 接受POST请求，若json中包含'id‘则查询改id用户的发布的任务
- 接收的json格式应包含
  - {‘id’: 用户的id}

- 查询失败返回json_false
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
根据发布者的用户名搜索任务API 

- 地址：'/search/sponsor’ 
- 接受POST请求
- 接收的json格式应包含
  - {‘sponsor’: 要查询的发起者的username}

- 查询失败返回json_false
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
根据任务标题进行模糊搜获API 

- 地址：'/search/title_key_word’ 
- 接受POST请求
- 接收的json格式应包含
  - {‘key_word’: 要查询的关键字}

- 查询失败返回json_false
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
推荐任务API 

- 地址：'/recommend’ 
- 接受POST请求
- 失败返回json_false
- 成功返回如下json：{'task_number':
					'task_id':[]}
- 备注：这个API事实上返回了所有发布中的任务，推荐顺序跟task_id中的排序一致

-----
根据任务详情进行模糊搜获API 

- 地址：'/search/detail_key_word’ 
- 接受POST请求
- 接收的json格式应包含
  - {‘key_word’: 要查询的关键字}

- 查询失败返回json_false
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----

根据id获得任务详情API 

- 地址：'/search/task_id’ 

- 接受POST请求

- 接收的json格式应包含

  - {‘task_id’: 任务的id}

- 查询失败返回json_false

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

- 查询失败返回json_false

- 查询成功返回如下json：{'id':

  ​					"username":
  ​					'email':

  ​					'school':

  ​					'major':

  ​					'phone':

  ​					'wx_number':

  ​					'hobbit':

  ​					}