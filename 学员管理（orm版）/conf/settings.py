#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
from sqlalchemy import create_engine

MYSQL_HOST_INFO = {'ip': '10.200.20.110', 'ssh_port': 22, 'username': 'root', 'password': '1234'}
DB_URI = 'mysql+pymysql://root:1235@10.200.20.110/stu_db?charset=utf8'
engine = create_engine(DB_URI, encoding='utf-8')