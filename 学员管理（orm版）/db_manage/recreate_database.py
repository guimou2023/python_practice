import paramiko
from conf.settings import MYSQL_HOST_INFO
# from core import init_db


# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname=MYSQL_HOST_INFO['ip'], port=MYSQL_HOST_INFO['ssh_port'], username=MYSQL_HOST_INFO['username'], password=MYSQL_HOST_INFO['password'])

# 执行命令
stdin, stdout, stderr = ssh.exec_command("mysql  -p{} -e 'drop database if exists stu_db;create database stu_db charset utf8;'".format(MYSQL_HOST_INFO['mysql_password']))
# 获取命令结果
result_stdout = stdout.read()
result_stderr = stderr.read()
result = result_stdout if result_stdout else result_stderr

print(result.decode())

# 关闭连接
ssh.close()