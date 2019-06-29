# API调用文档

[TOC]

-----

> 注意：每次“需要登录”的api在使用的过程中，都需要在headers里面加入session_id和user_id，作为身份验证的一个辅助手段。session_id在每次登陆的时候都会返回。

## User

### 注册

- 地址：'/register' 

- 接受POST请求

- 接收的json格式应包含


    {‘id’: 
    
    'username':
    
    'email':
    
    'school':
    
    'major':
    
    'phone':
    
    'wx_number':
    
    'hobbit':
    
    }

- 注册成功返回json_true, 失败则返回包含‘errmsg’的json文件

----

### 登陆

- 地址：'/login' 

- 接受POST请求

- 接收的json格式应包含
  ```
    {‘id’: 
  'password':}
  ```
  
  登陆成功返回当前对话的session_id, 失败则返回包含‘errmsg’的json文件
-----
### 登出（需要登录） 

- POST
- 地址：'/logout' 
- 成功登出返回json_true并删除之前建立的session。

---

### 修改任务（需要登录）

- 地址：'/modify/user_info' 

- 接受POST请求

- 接收的json格式应包含

  {‘id’: }以及其他修改信息如username，email，school，major，phone，wx_number，hobbit

- 成功则返回修改后的user数据，失败则返回包含‘errmsg’的json文件

---

### 修改用户信息（需要登录）

- 地址‘/modify/user_info’

- 接收POST请求

- 接收的json必须包含‘id’信息，可包含以下信息

  ```
  ‘username’:
  ‘email’:
  ‘school’:
  ‘major’:
  ‘phone’:
  ‘wx_number’:
  ‘hobbit’:
  'profile':
  ```

  修改成功返回user信息json（与查询user信息APIi一致），失败返回包含‘errmsg’的json

---

### 修改密码（需要登录）

- 地址：'/password' 

- 接受POST请求

- 接收的json格式应包含

  ```
  {‘id’: 
    'password':}
  ```

  成功则返回`修改密码成果`，失败则返回包含‘errmsg’的json文件

---

### 上传头像

- 地址：'/postProfile' 

- 接受POST请求

- 使用小程序的uploadfile的方法将图像上传

  文件名称：image

  附带：task_id

- 成功则返回提交后存储的文件名，失败则返回包含‘errmsg’的json文件

---

### 返回头像

- 地址：'/user/<imagename>' 
- 接受POST请求
- 接受上面上传头像之后的文件名，也可以查询用户的信息，在profile中提取，返回url

- 使用：直接把url放在前端解决

---

### 查看钱包状态

- 地址：'/wallet' 

- 接受POST请求

```
{id:}
```

- 返回用户的账号余额，支出和收入

---

### 充值

- 地址：'/recharge' 

- 接受POST请求

  ```
  {id:
    value:}
  ```

  返回用户的账号余额

---

### 提现

- 地址：'/withdraw' 
- 接受POST请求

```
{
	id:
	value:
}
```

- 返回用户的账号余额

---

### 验证邮箱

- 地址：‘/sendemailcode’

- 接受POST请求

  ```python
  {
      'code':
      'target_email':
  }
  ```

---



## Task

### 发布任务(需要登录)

- 地址：'/task/sponsor' 

- 接受POST请求

- 接收的json格式应包含
  ```python
  {
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
  ```
  
  - questions是一个存储问题的list，比如 ['abc', 'dd']
  - options是一个存储选项的list,每个元素也是一个list，存储对应问题的选项，如果对应问是个问答题，则，则对应的元素是一个空list，比如 [ ['a', 'b', 'c'],  ['a', 'b'] , [] ] （第三题是问答题）
  - types是一个list，用记录对应问题是单选/多选/问答
  
- 注册成功返回json_true, 失败则返回包含‘errmsg’的json文件

-----
### 接收任务（需要登录）

- 地址：'/task/receive' 
- 接受POST请求，要求用户先登录才能接收任务
- 接收的json格式应包含

  - {‘id’: 任务的id}

- 注册成功返回json_true, 失败则返回包含‘errmsg’的json文件
---

### 用户提交问卷答案

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

---

### 退出任务

- 地址:'/task_quit'
- 接收POST请求
- 接收如下json
  {
    'user_id':
    'task_id':
  }
- 退出成功返回json_true，失败返回包含‘errmsg’的json文件

---

### 取消任务

- 地址: '/task_cancel'
- 接收POST请求
- 接收如下json
  {
    'user_id':
    'task_id':
  }
- 退出成功返回json_true, 失败返回包含‘errmsg’的json文件

---

### 上传任务图片

- 地址：
- 接受POST请求
- 使用小程序的uploadfile的方法，传递图片，图片在’image‘中，上传的任务id在‘task_id’中

- 成功则返回上传后存储的文件名，用于后来直接访问图片，失败则返回包含‘errmsg'的json

---

### 返回图片

- 地址：'/task/<imagename>'
- 接受POST请求
- 直接将图片的名字（包含.jpg）代替imagename，即可直接访问图片。

- 成功则返回一个包含图片信息的response，可以直接在<img>标签中使用，失败则返回包含‘errmsg'的json

---

### 任务完成

- 地址：‘/task/finished’

- 接受POST请求

- json格式：

  ```python
  {
      user_id:
      task_id:
  }
  ```

- 成功则返回json_true，失败则返回包含‘errmsg'的json

---

### 支付

- 地址：‘/task/pay’

- 接受POST请求

- json格式：

  ```python
  {
      user_id:
      task_id:
  }
  ```

- 成功则返回json_true，如果任务已经全部完成并支付，则返回任务已完成，失败则返回包含‘errmsg'的json

---

### 修改任务信息

- 地址：‘/modify/task_info’

- 接受POST请求

- json格式：

  ```python
  #除了id其他均为可选
  {
  'id':
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
  ```

- 成功则返回json_true，失败则返回包含‘errmsg'的json（成功则会重新收取费用）

## Search

### 任务广场推荐任务

- 地址：'/recommend’ 

- POST或GET

  ```
  # 均为可选
  {
      batch_size :
      type:new' or 'hot'
  }
  ```

  

- 失败返回包含‘errmsg’的json文件

- 成功返回如下json：{'task_number':
  				'task_info':[ {‘id’:  'title':   'detal':    'type':   }, {‘id’:  'title':   'detal':    'type':   } , ... ]}

- 备注：这个API事实上返回了所有发布中的任务，推荐顺序跟task_id中的排序一致

---

### 查看发布的任务

- 地址：'/task/mysponsor' 
- 接受POST请求，若json中包含'id‘则查询改id用户的发布的任务，若无’id‘属性，则查询当前登陆用户的发布任务'
- 接收的json格式应包含
  - {‘id’: 用户的id}

- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
  				'task_id':[]}
-----
### 查看接收的任务

- 接受POST请求，要求用户先登录才能查看，可以传入查询的用户id，如果没有传入，则查询当前用户的接受任务
- 地址：'/task/myreceive‘' 
- 接受POST请求，若json中包含'id‘则查询改id用户的发布的任务
- 接收的json格式应包含
  - {‘id’: 用户的id}
- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
### 根据发布者的用户名搜索任务

- 地址：'/search/sponsor’ 
- 接受POST请求
- 接收的json格式应包含
  - {‘sponsor’: 要查询的发起者的username}

- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
### 根据任务标题进行模糊搜获

- 地址：'/search/title_key_word’ 
- 接受POST请求
- 接收的json格式应包含
  
- {‘key_word’: 要查询的关键字
  
    'batch_size':（可选）需要获得的task个数，没有传递则返回全部}
  
- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----
### 根据任务详情进行模糊搜获

- 地址：'/search/detail_key_word’ 
- 接受POST请求
- 接收的json格式应包含
  
- {‘key_word’: 要查询的关键字
  
    'batch_size':（可选）需要获得的task个数，没有传递则返回全部}
  
- 查询失败返回包含‘errmsg’的json文件
- 查询成功返回如下json：{'task_number':
					'task_id':[]}
-----

### 根据id获得任务详情

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
### 根据id获得用户详情

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

### 根据id获得问卷模板

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

----
### 根据任务接收者uid和任务id查询问卷答案

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

### 根据任务接收者user_id和任务id查询任务接受者情况

- 地址：'/search/receiver’ 

- POST

  ```
  {
      user_id :
  	task_id:    
  }
  ```

  

- 失败返回包含‘errmsg’的json文件

- 成功返回如下

  ```
  {
      isfinished:
      ispaid:
  }
  ```

---

### 根据任务task_id查看任务接受者的状态

- 地址：'search/myreceiver' 

- POST

  ```
  {
      receiver_id:
      receiver_name:
      receiver_isfinished:
      receiver_ispaid:
  }
  ```

  

- 失败返回包含‘errmsg’的json文件

- 成功返回如下json：{'task_number':
  				'task_info':[ {‘id’:  'title':   'detal':    'type':   }, {‘id’:  'title':   'detal':    'type':   } , ... ]}

---

### 根据任务类型进行搜索

- 地址：'/task_type/<task_type>’ 

- POST或GET

- 不用在Post中传递信息或者传递batch_size，使用task_type替代task_type即可。已知的类型有

  ```
  alltype = ['线上：问卷调查',
          '线上：信息标注',
          '线上：其他',
          '线下：快递代取',
          '线下：课程实验，访谈',
          '线下：跑腿',
          '线下：单次兼职',
          '线下：其他']
  ```

- 成功则返回所有的任务的id。