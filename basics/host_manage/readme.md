# 这是一个多进程的简单主机管理程序

### 作者介绍：
* author：Howard
* My Blog: [http://987774031.blog.51cto.com/](http://987774031.blog.51cto.com)  
* GitHub: [https://github.com/wuwuming/python_practice/tree/master/host_manage](https://github.com/wuwuming/python_practice/tree/master/host_manage)  

### 需求：  
- [x] 1. 运行程序列出主机组或者主机列表
- [x] 2. 选择指定主机或主机组
- [x] 3. 选择让主机或者主机组执行命令或者向其传输文件（上传/下载）
- [x] 4. 充分使用多线程或多进程
- [x] 5. 不同主机的用户名密码、端口可以不同

### 功能介绍：   
- 登陆后选择操作的主机组,键入主机组后进入操作菜单

  ```
      q ：退出
      xxx : 在被管理主机上执行xxx
      get filename ：下载文件
      put filename ：上传文件
  ```

- 程序运行端上传及下载的的目录为 run.py 文件所在目录，主机端目录为用户家目录

- 下载后文件保存为hostIP_filename

### 程序调试环境：  

* mac Python3.6

### 补充说明：
* 程序很简单，所以流程图又省略拉


