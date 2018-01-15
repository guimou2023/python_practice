# 这是一个多主机异步执行命令程序

### 作者介绍：
* author：Howard
* My Blog: [http://987774031.blog.51cto.com/](http://987774031.blog.51cto.com)  
* GitHub: [https://github.com/wuwuming/python_practice/tree/master/machine_manage](https://github.com/wuwuming/python_practice/tree/master/machine_manage)  

### 需求：  

```
例子：
>>:run "df -h" --hosts 192.168.3.55 10.4.3.4 
task id: 45334
>>: check_task 45334 
>>: 
注意，每执行一条命令，即立刻生成一个任务ID,不需等待结果返回，通过命令check_task TASK_ID来得到任务结果 
```

### 功能介绍：   
先运行server.py,再运行client.py,

键入`run 'ls' --hosts 10.1.1.170 10.1.1.192`或`run "ls" --hosts 10.1.1.170 10.1.1.192`，

立即返回`task_id: 1515977xxx`，

键入`check_task 1515977xxx`获取命令执行结果，

如结果还未返回，则提示“正在获取结果，稍后再试。。。”

### 实现说明：

* 收发消息使用rabbitmq队列存储
* 客户端传递消息时为避免阻塞，使用了守护线程
* 服务端连接受管主机使用了多进程，为了聚合多主机执行命令结果，使用了进程间通信

### 程序调试环境：  
* mac Python 3.6
* PyCharm 2016.2
* Rabbitmq 3.6.14

### 补充说明：
* 未做异常捕获，个别情况可能不尽人意

