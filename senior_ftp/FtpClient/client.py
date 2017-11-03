#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# AUTHOR:Howard hao
import socket,json,os,sys,time,io
from hashlib import md5

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class FtpClient(object):

    def __init__(self):
        self.client = socket.socket()
        self.login_user = None

    def help(self):
        """帮助"""
        msg = '''
        ls : 查看服务端目录下文件
        ls client : 查看客户端当前目录下文件
        get filename : 下载文件
        put filename : 上传文件
        q : 退出
        cd .. : 进入家目录的上一层目录
        cd : 返回家目录
        非菜单输入：显示帮助
        '''
        print(msg)

    def authenticate(self):
        """认证"""
        login_data = dict()
        login_data['name'] = input('账号:').strip()
        self.login_user = login_data['name']
        login_data['passwd'] = input('密码:').strip()
        self.client.send(json.dumps(login_data).encode())
        a = (self.client.recv(1024)).decode()
        return a
        # print(self.client.recv(1024).decode())

    def connect(self,ip,port):
        """连接服务端"""
        self.client.connect((ip, port))

    def interactive(self):
        """交互"""
        if self.authenticate() == 'ok':
            print(u'登录成功！')
            self.help()
            while True:
                cmd = input(">>").strip()
                if len(cmd) ==0:
                    self.help()
                    continue
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

    @staticmethod
    def view_bar(num, total):
        rate = num / total
        rate_num = int(rate * 100)
        r = '\r[%s%s]%d%%' % ("#" * num, " " * (100 - num), rate_num,)
        sys.stdout.write(r)
        sys.stdout.flush()

    def cmd_put(self,*args):
        """上传"""
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dic = {
                    "action": "put",
                    "filename":filename,
                    "size": filesize,
                    "overridden":True,
                }
                self.client.send(json.dumps(msg_dic).encode("utf-8"))
                # print("send",json.dumps(msg_dic).encode("utf-8") )
                #防止粘包，等服务器确认
                server_response = self.client.recv(1024)
                server_response_data = server_response.decode()
                if server_response_data != '200 ok':
                    self.cmd_status(server_response_data)
                else:
                    f = open(filename, "rb")
                    send_size = 0
                    num = 0
                    for line in f:
                        self.client.send(line)
                        send_size += len(line)
                        num += 1
                        if num == 15 and send_size <= filesize:
                            FtpClient.bar(send_size,filesize)
                            num = 0
                    else:
                        f.flush()
                        f.close()
                        FtpClient.bar(send_size, send_size)
                        rec = self.client.recv(1024).decode()
                        print('\n文件 %s 上传成功...' % filename)
                        print('client md5:%s' % (self.md5_func(filename)))
                        print('server md5:%s' % rec)
                        if self.md5_func(filename) == rec:
                            print('上传文件 md5 认证通过！')
                        else:print('上传文件 md5 认证失败！')

            else:
                print('当前目录下',filename,"is not exist")

    def cmd_get(self,*args):
        """下载"""
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
                    b = ['y', 'Y', 'Yes', 'yes', '']
                    if a in b:
                        self.client.send('知道啦，老铁'.encode())
                        f = open(filename, "wb")
                        received_size = 0
                        num = 0
                        while received_size < server_response_dic['size']:
                            data = self.client.recv(1024)
                            f.write(data)
                            received_size += len(data)
                            num += 1
                            if num == 15 and received_size <= server_response_dic['size']:
                                FtpClient.bar(received_size,server_response_dic['size'])
                                num = 0
                        else:
                            FtpClient.bar(received_size,received_size)
                            f.flush()
                            f.close()
                            print('\n文件 %s 下载成功...' %filename)
                            print('server md5:%s' %(server_response_dic['md5']))
                            print('client md5:%s' %(self.md5_func(filename)))
                            if server_response_dic['md5'] == self.md5_func(filename):
                                print('下载文件 md5 认证通过！')
                            else:print('下载文件 md5 认证失败！')

                else:
                    self.client.send('知道啦，老铁'.encode())
                    f = open(filename, "wb")
                    received_size = 0
                    num = 0
                    while received_size < server_response_dic['size']:
                        data = self.client.recv(1024)
                        f.write(data)
                        received_size += len(data)
                        num += 1
                        if num == 15 and received_size <= server_response_dic['size']:
                            FtpClient.bar(received_size, server_response_dic['size'])
                            num = 0
                    else:
                        FtpClient.bar(received_size,received_size)
                        sys.stdout.write(' 100%\n')
                        sys.stdout.flush()
                        f.close()
                        print('文件 %s 下载成功...' % filename)
                        print('server md5:%s' % (server_response_dic['md5']))
                        print('client md5:%s' % (self.md5_func(filename)))
                        if server_response_dic['md5'] == self.md5_func(filename):
                            print('md5 认证通过！')
                        else:
                            print('md5 认证失败！')

    def cmd_ls(self,*args):
        """查看家目录"""
        msg_dic = {
            "action": "ls_home",
            "filename": None,
        }
        cmd = args[0].split()
        if len(cmd) == 1:
            self.client.send(json.dumps(msg_dic).encode())
            cmd_res_data = self.client.recv(1024)
            print(cmd_res_data.decode())
        elif len(cmd) == 2 and cmd[1] == 'client':
            os.system('ls -l')

    def cmd_cd(self,*args):
        cmd_list = args[0].split()
        msg_dic = {
            "action": "update_tmp_path",
            "path": None,
        }
        if len(cmd_list) == 1:
            msg_dic["path"] = 'home'
            self.client.send(json.dumps(msg_dic).encode())
            print('回到家目录！')
        elif len(cmd_list) == 2 :
            if cmd_list[1] == '..':
                msg_dic["path"] = 'parent'
                self.client.send(json.dumps(msg_dic).encode())
                print('切换至家目录的父目录！')
            elif cmd_list[1] == self.login_user:
                msg_dic["path"] = 'home'
                self.client.send(json.dumps(msg_dic).encode())
                print('回到家目录！')
            else:print('无访问权限！')

    def cmd_status(self,*args):
        """状态展示"""
        status_data = json.loads(args[0])
        status_dict = {'403':'上传文件大小达到限额，上传失败，请联系管理员扩容。'}
        print(status_dict[status_data['status_code']])

    @staticmethod
    def bar(trans_data, total):
        rate = trans_data / total
        count = int(rate * 100)
        space_num = 100 - count
        r = '\r[%s%s]%d%%' % ("#" * count, " " * space_num, count)
        sys.stdout.write(r)
        sys.stdout.flush()

    def md5_func(self,filepath):
        m = md5()
        # 需要使用二进制格式读取文件内容
        a_file = open(filepath, 'rb')
        m.update(a_file.read())
        a_file.close()
        return m.hexdigest()


ftp = FtpClient()
ftp.connect("localhost",9998)
ftp.interactive()
