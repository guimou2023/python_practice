#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import socket,select,queue
import json,os

BaseDir = os.path.dirname(os.path.abspath(__file__))
UserDdir = os.path.join(BaseDir, 'user_db')
FileDir = os.path.join(BaseDir, 'file_db')


def authenticate(auth_data, conn):
    """用户登陆认证"""
    auth_dict_data = json.loads(auth_data.decode())
    print(auth_dict_data)
    user_path = os.path.join(UserDdir, auth_dict_data['name'])
    if os.path.isfile(user_path):
        with open(user_path, 'r', encoding='utf-8') as f:
            record_data = json.load(f)
        if record_data['passwd'] == auth_dict_data['passwd']:
            conn.send('ok'.encode())
            return True
        else:
            conn.send('not'.encode())
    else:
        conn.send('not'.encode())


def main():
    """主函数"""
    server = socket.socket()
    server.bind(('localhost', 9001))
    server.listen(9001)
    server.setblocking(0)  # socket设定非阻塞模式

    inputs = [server, ]
    outputs = []

    msg_dic = {}  #存储队列的字典
    name_dict = {}  #存储登陆用户名字的字典
    file_name_dict = {}  #存储传输文件名字的字典
    file_size = {}  #存储传送文件大小信息
    authorized = []  #登陆认证通过连接存储列表
    status_dict = {}  #存储服务端与客户端当前交互状态字典

    while True:
        readable, writeable, exceptional = select.select(inputs, outputs, inputs)
        for r in readable:
            if r is server:
                conn, addr = server.accept()
                print("来了个新连接", addr)
                inputs.append(conn)
                msg_dic[conn] = queue.Queue()  #初始化一个队列，后面存要返回给这个客户端的数据

            else:
                if r in authorized:
                    data = r.recv(1024)
                    if data:
                        if status_dict[r] is None:  #状态为 None 说明是收到一个新动作，向客户端发送ack，防止粘包
                            r.send(b'ack')
                        msg_dic[r].put(data)
                        if r not in outputs:
                            outputs.append(r)
                    else:
                        if r in outputs:
                            outputs.remove(r)

                else:
                    data = r.recv(1024)
                    if data:
                        cmd_dic = json.loads(data.decode())
                        action = cmd_dic["action"]
                        name = cmd_dic["name"]
                        if action == 'auth':
                            if authenticate(data, conn):
                                name_dict[r] = name
                                authorized.append(r)
                                status_dict[r] = None
                                print(r, '认证通过')
                            else:
                                inputs.remove(r)
                                del msg_dic[r]
        for w in writeable:
            if w in outputs:
                if status_dict[w] == 'put':
                    filename = file_name_dict[w]
                    file_path = os.path.join(FileDir, name_dict[w], filename)

                    try:
                        f = open(file_path, "ab")
                        b_data = msg_dic[w].get_nowait()
                    except queue.Empty:
                        if w in outputs:
                            outputs.remove(w)
                        print('file {} upload success...'.format(file_name_dict[w]))
                        status_dict[w] = None
                        file_name_dict[w] = None
                        f.close()
                    else:
                        f.write(b_data)
                        f.close()
                elif status_dict[w] == 'get':
                    filename = file_name_dict[w]
                    file_path = os.path.join(FileDir, name_dict[w], filename)
                    server_file_size = 0
                    if os.path.exists(file_path):
                        server_file_size = os.stat(file_path).st_size
                    if file_size[w] < server_file_size:
                        f = open(file_path, "rb")
                        f.seek(file_size[w])
                        for line in f:
                            w.send(line)
                            file_size[w] += len(line)
                            break
                        f.close()
                    else:
                        print("file {} download success...".format(filename))
                        if w in file_name_dict:
                            file_name_dict[w] = None
                        if w in status_dict:
                            status_dict[w] = None

                else:
                    try:
                            b_data = msg_dic[w].get_nowait()
                            outputs.remove(w)
                    except queue.Empty:
                        if w in outputs:
                            outputs.remove(w)
                    else:
                        print('b_data', b_data.decode('utf-8'))
                        data = json.loads(b_data.decode('utf-8'))
                        if data['action'] == 'put':
                            file_name_dict[w] = data["filename"]
                            status_dict[w] = 'put'
                            file_size[w] = data['size']
                        elif data['action'] == 'get':
                            if data['status'] == 'first':
                                file_size[w] = 0
                                file_name_dict[w] = data["filename"]
                                status_dict[w] = 'get'
                                m_dic = {
                                    "action": "get",
                                    "filename": data["filename"],
                                    "size": None,
                                    "exist": False
                                }
                                file_path = os.path.join(FileDir, name_dict[w], file_name_dict[w])
                                if not os.path.isfile(file_path):
                                    print('not exist')
                                    print('send ', m_dic)
                                    w.send(json.dumps(m_dic).encode())
                                    if w in file_name_dict:
                                        file_name_dict[w] = None
                                    if w in status_dict:
                                        status_dict[w] = None
                                else:
                                    m_dic['exist'] = True
                                    m_dic['size'] = os.stat(file_path).st_size
                                    w.send(json.dumps(m_dic).encode())
                            else:
                                print(data)

                        elif data['action'] == 'quit':
                            inputs.remove(w)
                            del name_dict[w]
                            if w in file_name_dict:
                                del file_name_dict[w]
                            if w in authorized:
                                authorized.remove(w)
                            if w in status_dict:
                                del status_dict[w]
                            print('连接{}断开'.format(w))

        for e in exceptional:
            if e in outputs:
                outputs.remove(e)
            inputs.remove(e)
            del msg_dic[e]
            del name_dict[e]

if __name__ == '__main__':
    main()