# 这是一个orm版学员管理程序

### 作者介绍：
* author：Howard
* My Blog: [http://987774031.blog.51cto.com/](http://987774031.blog.51cto.com)  
* GitHub:[代码地址](https://github.com/wuwuming/python_practice/tree/master/%E5%AD%A6%E5%91%98%E7%AE%A1%E7%90%86%EF%BC%88orm%E7%89%88%EF%BC%89)  

### 需求：  
- [x] 讲师视图和学员视图,根据用户名认证登陆
- [x] 讲师可进行班级管理(查看管理的班级列表、创建班级、创建课程)和学员管理(录入学员信息、修改学员成绩)
- [x] 学员通过班级名认证后，可以进行作业提交（提交时需选择班级及课程天数）和成绩查看（班级名认证通过后显示总成绩及班级内排名）


### 使用说明：

- 配置项在conf/settings.py中
- 使用前需初始化数据库，执行db_mansge下recreate_database.py建库，执行core下init_db.py建表,执行db_mansge下add_test_data.py添加测试数据

### 程序说明：

- 建表思路见目录下png文件

### 程序调试环境：  

* mac Python3.6

