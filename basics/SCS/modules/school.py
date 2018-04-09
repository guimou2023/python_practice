#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
from modules.student import Student
from modules.course import Course
from modules.teacher import Teacher
from modules.class_mode import  ClassFunc


class School(object):
    """用于存储生成的学生对象、课程对象、讲师对象、班级对象"""
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.students = []
        self.teacher = []
        self.course = []
        self.classs = []

        self.teacher_name_list = []
        self.course_name_list = []
        self.class_name_list = []

    def create_student(self, name, age, course):
        '''
        添加学生至学校
        :param name: 姓名
        :param age: 年龄
        :param course: 选择的课程
        :return:
        '''
        # 添加学员至学校
        stu_obj = Student(name, age, course)
        # 获取学员对象姓名
        print("为学员%s 办理注册手续" % stu_obj.name)
        # 并把学员对象加入到学校的对象中
        self.students.append(stu_obj)

    def add_teacher(self, name, salary):
        teacher_obj = Teacher(name, salary)
        print("老师%s 信息录入成功。" % teacher_obj.name)
        self.teacher.append(teacher_obj)

    def add_course(self, course_name, course_period, course_cost):
        self.course.append(Course(course_name, course_period, course_cost))

    def add_class(self, class_name, class_course, teacher_name):
        self.classs.append(ClassFunc(class_name, class_course, teacher_name))

    def show_teacher(self):
        if len(self.teacher) > 0:
            print('已有讲师列表：')
            for j in self.teacher:
                print(j.name)
                self.teacher_name_list.append(j.name)
            else:
                return self.teacher_name_list
        else:
            return []

    def show_course(self):
        if len(self.course) > 0:
            print('已有课程列表：')
            for j in self.course:
                print(j.course_name)
                self.course_name_list.append(j.course_name)
            else:
                return self.course_name_list
        else:
            return []

    def show_class(self):
        if len(self.classs) > 0:
            print('已有班级列表：')
            for j in self.classs:
                print(j.class_name)
                self.class_name_list.append(j.class_name)
                return self.class_name_list
        else:
            return []


