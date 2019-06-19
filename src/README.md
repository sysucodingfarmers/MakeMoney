# Code for our project
<hr/>
<font size=4 face="黑体">
1) clone项目到本地，以Desktop为例

	git clone https://github.com/sysucodingfarmers/MakeMoney.git

&nbsp;&nbsp;&nbsp;&nbsp;这样，在Desktop下就有了MakeMoney文件夹了
2) 在Desktop下，新建wepy项目，以名字为test为例。创建好后，进入test文件夹
	
	wepy init standard test
	cd test
	
3) 删去test文件夹下的dist和node_module文件夹
4) 将MakeMoney/src文件夹下的内容，移动并覆盖掉test文件夹下的内容
5) 将test文件夹的内容，移动回去MakeMoney/src
6) 在MakeMoney/src文件夹下，安装依赖

	npm install
7） 打开微信开发工具，导入MakeMoney/src
