#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"


class Student(object):
    """用于生成学生对象"""
    def __init__(self, name, balance, class_name):
        self.name = name
        self.balance = balance
        self.score = 0
        self.class_name = class_name

    def new_score(self, score):
        self.score = score
