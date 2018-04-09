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
        ls : 查看当前目录下文件
        ls home : 查看用户家目录下文件
        get filename : 下载文件
        put filename : 上传文件
        q : 退出
        '''
        print(msg)
    def authenticate(self):
        login_data = dict()
        login_data['name'] = input('账户名：').strip()
        login_data['passwd'] = input('密码：').strip()
        self.client.send(json.dumps(login_data).encode())
        a = (self.client.recv(1024)).decode()
        return a
        # print(self.client.recv(1024).decode())
    def connect(self,ip,port):
        self.client.connect((ip, port))
    def interactive(self):
        if self.authenticate() == 'ok':
            print('登录成功！')
            while True:
                self.help()
                cmd = input(">>").strip()
                if len(cmd) ==0:continue
                cmd_str = cmd.split()[0]
                if cmd == 'q':
                    self.client.send(json.dumps({'action':'quit'}).encode())
                    exit('Bye!')
                if hasattr(self,"cmd_%s" % cmd_str):
                    func = getattr(self,"cmd_%s" % cmd_str)
                    func(cmd)
                else:
                    self.help()
        else:exit('Error,authentication failed !')
    def cmd_put(self,*args):
        cmd_split =  args[0].split()
        if len(cmd_split) >1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dic = {
                    "action": "put",
                    "filename":filename,
                    "size": filesize,
                    "overridden":True
                }
                self.client.send( json.dumps(msg_dic).encode("utf-8")  )
                # print("send",json.dumps(msg_dic).encode("utf-8") )
                #防止粘包，等服务器确认
                server_response = self.client.recv(1024)
                f = open(filename,"rb")
                for line in f:
                    self.client.send(line)
                else:
                    print("file upload success...")
                    f.close()
            else:
                print(filename,"is not exist")
    def cmd_get(self,*args):
        cmd_list = args[0].split()
        if len(cmd_list) > 1:
            filename = cmd_list[1]
            msg_dic = {
                "action": "get",
                "filename": filename
            }
            self.client.send(json.dumps(msg_dic).encode("utf-8"))
            server_response = self.client.recv(1024)
            server_response_dic = json.loads(server_response.decode())
            if not server_response_dic['exist']:
                print('服务端该文件不存在')
            else:
                if os.path.isfile(filename):
                    print('此文件已存在当前目录，overwrite ?')
                    a = input('>>:').strip()
                    b = ['y', 'Y', 'Yes', 'yes']
                    if a in b:
                        self.client.send('知道啦，老铁'.encode())
                        f = open(filename, "wb")
                        received_size = 0
                        while received_size < server_response_dic['size']:
                            data = self.client.recv(1024)
                            f.write(data)
                            received_size += len(data)
                        else:
                            f.flush()
                            f.close()
                            print('文件:%s 下载成功' %filename)
                else:
                    self.client.send('知道啦，老铁'.encode())
                    f = open(filename, "wb")
                    received_size = 0
                    while received_size < server_response_dic['size']:
                        data = self.client.recv(1024)
                        f.write(data)
                        received_size += len(data)
                    else:
                        f.close()
                        print('文件:%s 下载成功' % filename)

    def cmd_ls(self,*args):
        msg_dic = {
            "action": "ls_home",
            "filename": None,
        }
        cmd = args[0].split()
        if len(cmd) == 2 and cmd[1] == 'home':
            self.client.send(json.dumps(msg_dic).encode())
            cmd_res_data = self.client.recv(1024)
            print(cmd_res_data.decode())
        else:
            os.system('ls')


ftp = FtpClient()
ftp.connect("localhost",9995)
ftp.interactive()
