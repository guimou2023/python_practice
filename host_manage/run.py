#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
import paramiko, re
from multiprocessing import Process

"""
主机组配置：对应的为端口、用户名、登陆密码
"""
config = {'0': [22, 'hh', '1234'],
          '1': [22, 'hh', '1234']}

"""主机组列表"""
host_group = {
    'g1': {'config_id': '0', 'ip_list': ['10.200.20.90', '10.200.20.85']},
    'g2': {'config_id': '1', 'ip_list': ['10.200.20.84', '10.200.20.83']},
}


class Manage(object):

    def __init__(self, ip, *args):
        self.ip = ip
        self.config = args[-1]
        self.action = args[0]
        self.action_split = self.action.split()
        if re.search('put|get', self.action) and hasattr(self, self.action_split[0]):
            func = getattr(self, self.action_split[0])
            func(self.action_split[1])
        else:
            self.cmd(self.action)

    def cmd(self, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip, port=self.config[0], username=self.config[1], password=self.config[2])
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result_stdout = stdout.read()
        result_stderr = stderr.read()
        result = result_stdout if result_stdout else result_stderr
        print('\033[1;33m主机：{}\033[0m'.format(self.ip))
        print('\033[1;34m{}\033[0m'.format(result.decode()))
        ssh.close()

    def get(self, file_name):
        transport = paramiko.Transport((self.ip, self.config[0]))
        transport.connect(username=self.config[1], password=self.config[2])
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get('/home/{}/{}'.format(self.config[1], file_name), 'from_{}_{}'.format(self.ip, file_name))
        transport.close()
        print('\033[1;32m主机:{} 下载 {} 成功，重命名为 {}_{}\033[0m'.format(self.ip, file_name, self.ip, file_name))

    def put(self, file_name):
        transport = paramiko.Transport((self.ip, self.config[0]))
        transport.connect(username=self.config[1], password=self.config[2])
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('{}'.format(file_name), '/home/{}/{}'.format(self.config[1], file_name))
        transport.close()
        print('\033[1;32m主机:{} 上传 {} 成功。\033[0m'.format(self.ip, file_name))


def run():
    menu = '''
    q ：退出
    xxx : 在被管理主机上执行xxx
    get filename ：下载文件
    put filename ：上传文件
    '''
    while True:
        for i in host_group:
            print('\033[1;33m主机组{}:\033[0m'.format(i))
            for j in host_group.get(i)['ip_list']:
                print('\033[1;34m{}\033[0m'.format(j))
        group_id = input('想管理的主机组>>:').strip()
        if group_id == 'q':
            print('Bye')
            break
        elif group_id in host_group:
            config_msg = config[host_group[group_id]['config_id']]
            while True:
                print(menu)
                a = input('>>:').strip()
                if len(a) == 0:
                    continue
                elif a == 'q':
                    exit('Bye')
                for i in host_group.get(group_id)['ip_list']:
                    j = Process(target=Manage, args=(i, a, config_msg))
                    j.start()
                    j.join()

        else:
            print('主机组不存在')
            continue


run()
