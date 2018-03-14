#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
# from core.init_db import Student, Teacher, Class, Lession, StudentRecord
from sqlalchemy.orm import sessionmaker
from conf.settings import engine
from core.role import TeacherView, StuView


class Manage_system(object):

    def __init__(self):
        self.session = sessionmaker(engine)()
        self.handle()

    def handle(self):
        while True:
            user_choice = input('''\033[32;1m请输入您要登录的视图:
        1 讲师视图
        2 学员视图
        q 退出学员管理系统
        >>>\033[0m''')
            if user_choice == '1':
                TeacherView(self.session)
            elif user_choice == '2':
                StuView(self.session)
            elif user_choice == 'q':
                print("\033[33;1m感谢使用学员管理系统。\033[0m")
                break
            else:
                print("\033[31;1m请输入正确的选项！\033[0m")