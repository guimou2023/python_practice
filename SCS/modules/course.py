#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"


#课程类
class Course(object):
    """用于生成课程对象"""
    def __init__(self, course_name, course_period, course_cost):
        self.course_name = course_name
        self.course_period = course_period
        self.course_cost = course_cost
        self.class_list = []

