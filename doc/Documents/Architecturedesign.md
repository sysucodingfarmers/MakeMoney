## 架构设计
 架构分为三层：
- **前端用户层：** 用户通过微信小程序于我们的系统进行交互，交互界面提供注册登录、发布任务、接收任务、查询任务、问卷填写功能。
- **后端支持层：** 后端对系统的业务逻辑进行处理和控制，响应前端用户层的请求，实现各个模块的功能和提供接口。
- **数据库层：** 使用flask的SQLAlchemy对用户数据和业务数据进行可持久化的读取和存储。
![](https://raw.githubusercontent.com/sysucodingfarmers/MakeMoney/master/doc/Documents/pictures/%E6%9E%B6%E6%9E%84.png)
