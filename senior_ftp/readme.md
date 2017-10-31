# 这是一个简单ftp程序

### 作者介绍：
* author：haohe
* nickname:Howard
* My Blog:[http://987774031.blog.51cto.com/](http://987774031.blog.51cto.com)

### 功能介绍：
* 实现了登录认证、上传／下载文件，不通用户家目录不同
* 下载时文件若客户端已存在会提示是否覆盖，上传文件时若服务端已存在会保存于file.new中
* 可查看当前目录（FtpClient文件夹）下文件，用户家目录下文件
* 提供了ftp用户账号添加功能 user_add.py
* 服务端程序 server.py,客户端程序 client.py
* 初始有两个ftp登录账户(abc/abc，123/123)
* 验证上传功能时，上传后需点击账户家目录文件夹刷新才能看到新文件
### 环境依赖：
* Python3.0+

###程序调试环境：
* mac
