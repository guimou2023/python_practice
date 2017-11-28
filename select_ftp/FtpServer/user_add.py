#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import json,os

BaseDir = os.path.dirname(os.path.abspath(__file__))
UserDdir = BaseDir + '/user_db'
FileDir = BaseDir + '/file_db'

login_data = dict()
login_data['name'] = input('账户名：').strip()
login_data['passwd'] = input('密码：').strip()
user_path = UserDdir + '/' +login_data['name']
if not os.path.isfile(user_path):
    with open(user_path,'w',encoding='utf-8') as f:
        json.dump(login_data,f)
    os.mkdir(os.path.join(FileDir,login_data['name']))
