#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"


class Teacher(object):
    """用于生成讲师对象"""
    def __init__(self, name, salary):
        self.bind_class_name = False
        self.name = name
        self.salary = salary

    def bind_class(self, class_name):
        self.bind_class_name = class_name

