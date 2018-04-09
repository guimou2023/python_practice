#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"


class ClassFunc(object):
    """用于生成班级对象"""
    def __init__(self, class_name, class_course, teacher_name):
        self.class_name = class_name
        self.class_course = class_course
        self.teacher = teacher_name
