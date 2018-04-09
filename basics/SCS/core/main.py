#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"

import os
import shelve
from modules.student import Student
from modules.school import School
from conf.settings import DB_DIR
# if platform.system() == 'linux' or platform.system() == 'Darwin':
#     BASE_DIR = pathlib.Path(__file__).parent.parent
# DB_DIR = os.path.join(BASE_DIR, 'db', 'record.db')


def run():
    """数据不存在时初始化db，初始化两个校区及三门课程"""
    if not os.path.exists(DB_DIR):
        write = shelve.open(DB_DIR)
        s_bj_obj = School('北京校区', '北京')
        s_sh_obj = School('上海校区', '上海')
        s_bj_obj.add_course('linux', '3个月', '8000')
        s_bj_obj.add_course('python', '4个月', '9000')
        s_sh_obj.add_course('go', '5个月', '10000')
        write['bj'] = s_bj_obj
        write['sh'] = s_sh_obj
        write.close()
    while True:
        user_choice = input('''\033[32;1m请输入您要登录的视图:
    1 管理视图
    2 教师视图
    3 学生视图
    q 退出学员管理系统
    >>>\033[0m''')
        if user_choice == '1':
            ManageView()
        elif user_choice == '2':
            TeacherView()
        elif user_choice == '3':
            StudentView()
        elif user_choice == 'q':
            print("\033[33;1m感谢使用学员管理系统\033[0m")
            break
        else:
            print("\033[31;1m请输入正确的选项\033[0m")


class ManageView(object):

    def __init__(self):
        self.write = shelve.open(DB_DIR)
        for i in self.write:
            print('\033[32;1m{}: {}\033[0m'.format(i, self.write[i].name))
        while True:
            school_key = input('想管理的学校>>:').strip()
            if school_key in self.write.keys():
                break
            else:
                print('输入错误，校区不存在！！！')
                continue
        school_obj = self.write[school_key]
        while True:
            user_choice = input('''\033[32;1m请选择下一步操作:
        1 创建讲师
        2 创建课程
        3 创建班级
        b 返回上一级目录
        >>>\033[0m''')
            if user_choice == '1':
                a = school_obj.show_teacher()
                teacher_name = input('新讲师姓名>>:').strip()
                if teacher_name == 'b':
                    break
                elif teacher_name in a:
                    print('该讲师已存在')
                    continue
                teacher_salary = input('新讲师工资>>:').strip()
                school_obj.add_teacher(teacher_name, teacher_salary)
                self.write.update({school_key: school_obj})
            elif user_choice == '2':
                a = school_obj.show_course()
                while True:
                    course_name = input('新课程名字：').strip()
                    if course_name == 'b':
                        break
                    elif course_name in a:
                        print('班级已存在！！！')
                        continue
                    elif course_name and course_name not in a:
                        course_period = input('新课程培训周期：').strip()
                        course_cost = input('新课程学费：').strip()
                        school_obj.add_course(course_name, course_period, course_cost)
                        self.write.update({school_key: school_obj})
                        print('课程{} 创建成功。'.format(course_name))

            elif user_choice == '3':
                if len(school_obj.teacher) == 0:
                    print('无可授课讲师，请联系管理员录入讲师信息！！！')
                else:
                    a = school_obj.show_course()
                    school_obj.show_class()
                    class_name = input('新班级名称>>:').strip()
                    if class_name == 'b':
                        break
                    while True:
                        class_course = input('班级对应课程>>:').strip()
                        if class_course in a:
                            break
                        else:
                            print('输入有误！！！')
                    b = school_obj.show_teacher()
                    while True:
                        teacher_name = input('新班级安排的的讲师>>:').strip()
                        if teacher_name in b:
                            break
                        else:
                            print('输入有误，该讲师不存在！！！')
                    for i in school_obj.teacher:
                        if i.name == teacher_name and not i.bind_class_name:
                            obj = i
                            obj.bind_class(class_name)
                            school_obj.teacher.remove(i)
                            school_obj.teacher.append(obj)
                            school_obj.add_class(class_name, class_course, teacher_name)
                            self.write.update({school_key: school_obj})
                            print('班级{} 创建成功。'.format(class_name))
                            break
                    else:
                        print('该讲师已有绑定的班级！！！')

            elif user_choice == 'b':
                break
            else:
                print("\033[31;1m请输入正确的选项\033[0m")

    def __del__(self):
        self.write.close()


class TeacherView(object):
    def __init__(self):
        self.write = shelve.open(DB_DIR)
        for i in self.write:
            print('\033[32;1m{}: {}\033[0m'.format(i, self.write[i].name))
        while True:
            school_key = input('想管理的学校>>:').strip()
            if school_key in self.write.keys():
                break
            else:
                print('输入错误，校区不存在！！！')
                continue
        school_obj = self.write[school_key]
        name = input('讲师姓名>>>:').strip()
        for teacher_obj in school_obj.teacher:
            if teacher_obj.name == name:
                while True:
                    user_choice = input('''\033[32;1m请选择下一步操作:
                1 查看信息
                2 修改学员成绩
                b 返回上一级目录
                >>>\033[0m''')
                    if user_choice == '1':
                        print('班级：{}'.format(teacher_obj.bind_class_name))
                        print('学员信息：')
                        for stu_obj in school_obj.students:
                            if stu_obj.class_name == teacher_obj.bind_class_name:
                                print('姓名：{}  成绩：{}'.format(stu_obj.name,stu_obj.score))
                    elif user_choice == '2':
                        change_stu_name = input('修改成绩学员>>:').strip()
                        new_score = input('修改后分数>>:').strip()
                        for stu_obj2 in school_obj.students:
                            if stu_obj2.name == change_stu_name and stu_obj2.class_name == teacher_obj.bind_class_name:
                                obj = stu_obj2
                                obj.new_score(new_score)
                                school_obj.students.remove(stu_obj2)
                                school_obj.students.append(obj)
                                self.write.update({school_key: school_obj})
                                print('修改成功！')
                                break
                        else:
                            print('输入有误！！！')

                    elif user_choice == 'b':
                        break
                    else:
                        print("\033[31;1m请输入正确的选项\033[0m")
                break
        else:
            print('该讲师不存在。')

    def __del__(self):
        self.write.close()


class StudentView(object):
    def __init__(self):
        self.write = shelve.open(DB_DIR)
        for i in self.write:
            print('\033[32;1m{}: {}\033[0m'.format(i, self.write[i].name))
        while True:
            school_key = input('想要学习的校区>>:').strip()
            if school_key in self.write.keys():
                break
            else:
                print('输入错误，校区不存在！！！')
                continue
        school_obj = self.write[school_key]
        school_obj.show_course()
        a = school_obj.show_class()
        if len(a) > 0:
            stu_name = input('姓名>>:').strip()
            balance = input('预存学费>>:').strip()
            while True:
                class_name = input('注册的班级>>:').strip()
                if class_name in a:
                    break
                else:
                    print('输入错误！！！')
            school_obj.students.append(Student(stu_name, balance, class_name))
            self.write.update({school_key: school_obj})
            print('学员：{} 注册成功！'.format(stu_name))
        else:
            print('无可选择班级，请联系管理员创建班级。')

    def __del__(self):
        self.write.close()


