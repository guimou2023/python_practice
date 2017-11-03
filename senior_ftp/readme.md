# 这是一个升级版ftp程序

### 作者介绍：
* author：Howard
* My Blog: [http://987774031.blog.51cto.com/](http://987774031.blog.51cto.com)  
* GitHub: [https://github.com/wuwuming/python_practice/tree/master/senior_ftp](https://github.com/wuwuming/python_practice/tree/master/senior_ftp)  

### 需求：  
- [x] 用户加密认证
- [x] 多用户同时登陆
- [x] 每个用户有自己的家目录且只能访问自己的家目录
- [x] 对用户进行磁盘配额、不同用户配额可不同
- [x] 用户可以登陆server后，可切换目录
- [x] 查看当前目录下文件
- [x] 上传下载文件，保证文件一致性
- [x] 传输过程中现实进度条
- [ ] 支持断点续传


### 功能介绍：   
##### 登陆后功能菜单：

        ls : 查看服务端目录下文件
        ls client : 查看客户端当前目录下文件
        get filename : 下载文件
        put filename : 上传文件
        q : 退出
        cd .. : 进入家目录的上一层目录
        cd : 返回家目录
        非菜单输入：显示帮助
* 需求中打勾的选项为实现选项
* 下载时文件若客户端已存在会提示是否覆盖，上传文件时若服务端已存在会保存于file.new中
* FtpClient文件夹为客户端当前目录
* 提供了ftp用户账号添加功能 user_add.py
* 服务端程序 server.py,客户端程序 client.py
* 初始有两个ftp登录账户(abc/abc abc账户家目录配额50M，123/123 123账户家目录配额5Byte)
* 验证上传功能时，上传后需点击账户家目录文件夹刷新才能看到新文件
* client.py 里#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  
mac 上调试有的系统需要打开，否则会报字符集错误


### 程序调试环境：  
* mac Python3.6

### 补充说明：
* 想继续往下学了，断点续传以后回头再实现吧，吼吼
* 程序很简单，连接建立后一直在一个实例化过程里交互，所以流程图也省略拉


