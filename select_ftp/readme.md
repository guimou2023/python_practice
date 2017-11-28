# 这是一个select版ftp程序

### 作者介绍：
* author：Howard
* My Blog: [http://987774031.blog.51cto.com/](http://987774031.blog.51cto.com)  
* GitHub: [https://github.com/wuwuming/python_practice/tree/master/select_ftp](https://github.com/wuwuming/python_practice/tree/master/select_ftp)  

### 需求：  
- [x] 用户加密认证
- [x] 多用户同时登陆
- [x] 每个用户有自己的家目录且只能访问自己的家目录
- [x] 允许多用户并发上传下载文件


### 功能介绍：   
##### 登陆后功能菜单：

        get filename : 下载文件
        put filename : 上传文件
        q : 退出
        非菜单输入：显示帮助
* FtpClient文件夹为客户端当前目录
* 提供了ftp用户账号添加功能 user_add.py
* 服务端程序 server.py,客户端程序 client.py
* 初始有两个ftp登录账户(abc/abc，123/123)


### 程序调试环境：  
* mac Python3.6

### 补充说明：
* 程序很简单，所以流程图又省略拉


