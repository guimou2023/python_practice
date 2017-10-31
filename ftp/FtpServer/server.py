#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao

import socketserver
import json,os

BaseDir = os.path.dirname(os.path.abspath(__file__))
UserDdir = os.path.join(BaseDir,'user_db')
FileDir = os.path.join(BaseDir,'file_db')

class MyTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self,*args,**kwargs):
        super(MyTCPHandler,self).__init__(*args,**kwargs)
        self.user_name = None
        self.data = None
        self.auth_user_data = None

    def authenticate(self,*args):
        self.auth_user_data = self.request.recv(1024)
        if not self.auth_user_data:
            print('客户端已断开...')
        else:
            auth_dict_data = json.loads(self.auth_user_data.decode())
            print(auth_dict_data)
            user_path = os.path.join(UserDdir,auth_dict_data['name'])
            if os.path.isfile(user_path):
                with open(user_path,'r',encoding='utf-8') as f:
                    record_data = json.load(f)
                if record_data['passwd'] == auth_dict_data['passwd']:
                    self.user_name = auth_dict_data['name']
                    self.request.send('ok'.encode())
                    return True
                else:
                    self.request.send('not'.encode())
            else:
                self.request.send('not'.encode())
    def put(self,*args):
        '''接收客户端文件'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        filesize = cmd_dic["size"]
        file_path = os.path.join(FileDir,self.user_name,filename)
        file_path_new = os.path.join(FileDir,self.user_name,filename) + ".new"
        if os.path.isfile(file_path):
            f = open(file_path_new,"wb")
        else:
            f = open(file_path,"wb")
        self.request.send(b"200 ok")
        received_size = 0
        while received_size < filesize:
            data = self.request.recv(1024)
            f.write(data)
            received_size += len(data)
        else:
            f.flush()
            f.close()
            print("file [%s] has uploaded..." % filename)
    def get(self,*args):
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        file_path = os.path.join(FileDir, self.user_name, filename)
        msg_dic = {
            "action": "get",
            "filename": filename,
            "size": None,
            "exist": False
        }
        if not os.path.isfile(file_path):
            self.request.send(json.dumps(msg_dic).encode())
        else:
            msg_dic['exist'] = True
            msg_dic['size'] = os.stat(file_path).st_size
            self.request.send(json.dumps(msg_dic).encode())
            client_respon = self.request.recv(1024)
            f = open(file_path, "rb")
            for line in f:
                self.request.send(line)
            else:
                print("file upload success...")
            f.close()
    def ls_home(self,args):
        ls_path = os.path.join(FileDir,self.user_name)
        cmd = 'ls %s' %ls_path
        cmd_res = os.popen(cmd).read()
        if len(os.listdir(ls_path)) == 0:
            cmd_res = 'Empty！'
        self.request.send(cmd_res.encode())

    def handle(self):

        if self.authenticate(self):
            while True:
                try:
                    self.data = self.request.recv(1024).strip()
                    print("{} wrote:".format(self.client_address[0]))
                    print(self.data)
                    cmd_dic = json.loads(self.data.decode())
                    action = cmd_dic["action"]
                    if action == 'quit':break
                    if hasattr(self,action):
                        func = getattr(self,action)
                        func(cmd_dic)
                except ConnectionResetError as e:
                    print("err",e)
                    break
if __name__ == "__main__":
    HOST, PORT = "localhost", 9995
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
