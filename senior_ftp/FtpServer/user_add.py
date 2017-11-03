#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import json,os,pathlib

BaseDir = pathlib.Path(__name__).parent
UserDdir = BaseDir / 'user_db'
FileDir = BaseDir / 'file_db'

login_data = dict()
login_data['name'] = input('账户名：').strip()
login_data['passwd'] = input('密码：').strip()
login_data['file_size_limit'] = int(input('家目录大小（单位 Mb）：').strip()) * 1048576
user_path = UserDdir / login_data['name']
if not os.path.isfile(user_path):
    with open(user_path,'w',encoding='utf-8') as f:
        json.dump(login_data,f)
    os.mkdir(FileDir / login_data['name'])