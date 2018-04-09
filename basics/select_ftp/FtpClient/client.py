#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import socket
import json
import os


class FtpClient(object):

    def __init__(self):
        self.client = socket.socket()

    def help(self):
        msg = '''
        get filename : 下载文件
        put filename : 上传文件
        q : 退出
        '''
        print(msg)

    def authenticate(self):
        login_data = dict()
        login_data['action'] = 'auth'
        login_data['name'] = input('账户名：').strip()
        login_data['passwd'] = input('密码：').strip()
        self.client.send(json.dumps(login_data).encode())
        a = (self.client.recv(1024)).decode()
        return a

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def interactive(self):
        if self.authenticate() == 'ok':
            print('登录成功！')
            while True:
                self.help()
                cmd = input(">>").strip()
                if len(cmd) == 0:
                    continue
                cmd_str = cmd.split()[0]
                if cmd == 'q':
                    self.client.send(json.dumps({'action': 'quit'}).encode())
                    exit('Bye!')
                if hasattr(self,"cmd_%s" % cmd_str):
                    func = getattr(self,"cmd_%s" % cmd_str)
                    func(cmd)
                else:
                    self.help()
        else:
            exit('Error,authentication failed !')

    def cmd_put(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dic = {
                    "action": "put",
                    "filename":filename,
                    "size": filesize,
                    "overridden": True
                }
                self.client.send(json.dumps(msg_dic).encode("utf-8"))
                #防止粘包，等服务器确认
                server_response = self.client.recv(1024)
                f = open(filename,"rb")
                for line in f:
                    self.client.send(line)
                else:
                    print("file upload success...")
                    f.close()
            else:
                print(filename, "is not exist")

    def cmd_get(self, *args):
        cmd_list = args[0].split()
        if len(cmd_list) > 1:
            filename = cmd_list[1]
            msg_dic = {
                "action": "get",
                "filename": filename,
                "status": "first"
            }
            self.client.send(json.dumps(msg_dic).encode("utf-8"))
            server_response_ack = self.client.recv(1024)
            server_response = self.client.recv(1024)
            server_response_dic = json.loads(server_response.decode())
            if not server_response_dic['exist']:
                print('服务端该文件不存在')
            else:
                msg = {
                    "action": "get",
                    "status": "ack"
                }

                self.client.send(json.dumps(msg).encode("utf-8"))
                f = open(filename, "wb")
                received_size = 0
                while received_size < server_response_dic['size']:
                    data = self.client.recv(1024)
                    f.write(data)
                    received_size += len(data)
                else:
                    f.close()
                    print('文件:%s 下载成功' % filename)


ftp = FtpClient()
ftp.connect("localhost", 9001)
ftp.interactive()
