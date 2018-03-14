#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
import sqlalchemy, random
from core.init_db import Student, Teacher, Class, Course, StudyRecord, Class_m2m_course


class TeacherView(object):

    def __init__(self, session):
        self.session = session
        if self.auth():
            self.handle()

    def auth(self):
        '''登陆认证'''

        while True:
            teacher_name = input('教师姓名>>:').strip()
            if teacher_name == "q":
                return False
            self.teacher_obj = self.session.query(Teacher).filter_by(teacher_name=teacher_name).first()
            if not self.teacher_obj:
                print("\033[31;1m输入错误，请重试！\033[0m")
                continue
            else:
                return True

    def handle(self):

        while True:
            teacher_choice = input('''\033[32;1m请键入功能序号:
        1 班级管理
        2 学员管理
        b 返回
        q 退出学员管理系统
        >>>\033[0m''')
            if teacher_choice == '1':
                while True:
                    class_choice = input('''\033[32;1m请键入功能序号:
                1 查看管理的班级列表
                2 新增班级
                3 添加课程
                b 返回
                q exit
                >>>\033[0m''')
                    if class_choice == '1':
                        getattr(self, 'class_lists')()

                    elif class_choice == '2':
                        getattr(self, 'create_class')()
                    elif class_choice == '3':
                        getattr(self, 'add_course')()
                    elif class_choice == 'b':
                        break
                    elif class_choice == 'q':
                        exit()
                    else:continue
            elif teacher_choice == '2':
                while True:
                    stu_menu = input('''\033[32;1m请键入功能序号:
                1 添加学员信息
                2 修改学员成绩
                b 返回
                q exit
                >>>\033[0m''')
                    if stu_menu == '1':
                        class_name = input('班级>>:').strip()
                        class_obj = getattr(self, 'if_class_exist')(class_name)
                        if class_obj:
                            stu_name = input('学员姓名>>:').strip()
                            stu_qq = input('学员qq>>:').strip()
                            stu_obj = Student(stu_name=stu_name, qq=stu_qq)
                            if self.session.query(Student).filter_by(stu_name=stu_name).first():
                                result = input('该学员信息已录入!是否继续加入班级（"Y" or "N"）>>:').strip()
                                if result == 'Y':
                                    class_obj.students.append(stu_obj)
                                    self.session.add(class_obj)
                                    self.session.commit()
                            else:
                                class_obj.students.append(stu_obj)
                                self.session.add_all([stu_obj])
                                self.session.commit()
                                print('学员信息添加成功！')
                        else:
                            print('班级不存在！')

                    elif stu_menu == '2':
                        getattr(self, 'modify_study_record')()
                    elif stu_menu == 'b':
                        break
                    elif stu_menu == 'q':
                        exit()
                    else:continue
            elif teacher_choice == 'b':
                break

    def class_lists(self):
        classes_obj = self.teacher_obj.classes
        for c in classes_obj:
            print('\033[35;1m班级：{} 开设课程：{}\033[0m'.format(c.class_name, c.course_name))

    def create_class(self):
        class_name = input('新班级名>>:').strip()
        data = self.session.query(Class).filter_by(class_name=class_name).all()
        if data:
            print('该班级已存在！！！')
        else:
            course_name = input('该班级开设的课程>>:').strip()
            class_obj = Class(class_name=class_name, course_name=course_name)
            class_obj.teachers = [self.teacher_obj]
            self.session.add(class_obj)
            self.session.commit()
            print('班级：{} 创建成功！'.format(class_name))

    def add_course(self):
        class_name = input('班级>>:').strip()
        class_obj = self.if_class_exist(class_name)
        if class_obj:
            if self.teacher_obj in class_obj.teachers:
                try:
                    class_id = class_obj.id
                    content = input('课程内容>>:').strip()
                    course_obj = Course(content=content)
                    self.session.add(course_obj)
                    day = input('将此节课程作为本班级的第几天授课内容>>:').strip()
                    course_id = self.session.query(Course).filter_by(content=content).first().id
                    class_m2m_course__obj = Class_m2m_course(class_id=class_id, day_id=day, course_id=course_id)
                    self.session.add(class_m2m_course__obj)
                    self.session.commit()
                    print('课程添加成功！')

                except sqlalchemy.exc.IntegrityError as b:
                    print('该天课程已经录入!')
                    self.session.rollback()
            else:
                print('看这里')
        else:
            print('该班级不存在！！！')

    def if_class_exist(self, class_name):
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()
        if class_obj:
            return class_obj
        else:
            return False

    def modify_study_record(self):
        class_name = input('班级名>>:').strip()
        class_obj = self.if_class_exist(class_name)
        if class_obj:
            print('此班级共授课 [{}] 天！'.format(len(class_obj.class_courses)))
            day_num = input('修改第几天作业成绩>>:').strip()
            if day_num.isdigit():
                class_m2m_course_obj = self.session.query(Class_m2m_course).filter_by(class_id=class_obj.id, day_id=day_num).first()
                if class_m2m_course_obj:
                    stu_name = input('学员姓名>>:').strip()
                    stu_obj = self.session.query(Student).filter_by(stu_name=stu_name).first()
                    if stu_obj:
                        if stu_obj in class_obj.students:
                            class_m2m_course_id = class_m2m_course_obj.id
                            query_study_record_obj = self.session.query(StudyRecord).filter_by(stu_id=stu_obj.id).filter_by(class_m2m_course_id=class_m2m_course_id).first()
                            if query_study_record_obj:
                                new_score = input('想将学员成绩修改为>>:').strip()
                                if new_score.isdigit():
                                    query_study_record_obj.score = int(new_score)
                                    print('成绩修改成功！')
                                    self.session.commit()
                                else:
                                    print('输入有误！')
                            else:
                                print('此学员为提交该天课程作业！')
                        else:
                            print('学员不在此班级！')
                    else:
                        print('学员不存在！')
                else:
                    print('该天没有开课！')
            else:
                print('输入不是数字！')
        else:
            print('班级不存在！！！')


class StuView(object):
    def __init__(self, session):
        self.session = session
        if self.auth():
            self.handle()

    def auth(self):
        '''登陆认证'''

        while True:
            self.stu_name = input('学生姓名>>:').strip()
            if self.stu_name == "q":
                exit()
            elif self.stu_name == "b":
                break
            else:
                self.stu_obj = self.session.query(Student).filter_by(stu_name=self.stu_name).first()
                if self.stu_obj:
                    return True
                else:
                    print("\033[31;1m输入错误，请重试！\033[0m")


    def handle(self):
        while True:
            stu_choice = input('''\033[32;1m请键入功能序号:
        1 作业提交
        2 成绩查看
        b 返回
        q 退出学员管理系统
        >>>\033[0m''')
            if stu_choice == '1':
                class_name = input('班级名>>:').strip()
                class_obj = self.if_class_exist(class_name)
                if class_obj:
                    print('此班级共授课 [{}] 天！'.format(len(class_obj.class_courses)))
                    day_num = input('提交第几天作业>>:').strip()
                    if day_num.isdigit():
                        class_m2m_course_obj = self.session.query(Class_m2m_course).filter_by(class_id=class_obj.id, day_id=day_num).first()
                        if class_m2m_course_obj:
                            stu_score = random.randint(60, 100)
                            class_m2m_course_id = class_m2m_course_obj.id
                            query_study_record_obj = self.session.query(StudyRecord).filter_by(stu_id=self.stu_obj.id).filter_by(class_m2m_course_id=class_m2m_course_id).first()
                            if query_study_record_obj:
                                print('作业已提交过,请勿重复提交！\n成绩：{}'.format(query_study_record_obj.score))
                            else:
                                study_record_obj = StudyRecord(class_m2m_course_id=class_m2m_course_id, stu_id=self.stu_obj.id, status='yes', score=stu_score)
                                self.session.add(study_record_obj)
                                self.session.commit()
                                print('作业提交成功！成绩：{}  \n有疑问请联系授课讲师！'.format(stu_score))
                        else:
                            print('该天没有开课！')
                    else:
                        print('输入不是数字！')
                else:
                    print('班级不存在！！！')
            elif stu_choice == '2':
                class_name = input('班级名>>:').strip()
                class_obj = self.if_class_exist(class_name)
                if class_obj:
                    if self.stu_obj in class_obj.students:
                        print('班级有学员 {} 名！'.format(len(class_obj.students)))
                        data = self.session.query(StudyRecord.stu_id, sqlalchemy.func.sum(StudyRecord.score)).outerjoin(Class_m2m_course, Class_m2m_course.id == StudyRecord.class_m2m_course_id).group_by(StudyRecord.stu_id).all()
                        rank = 1
                        no_study_record = True
                        for d in data:
                            if d[0] == self.stu_obj.id:
                                print('学号：{} 姓名：{} 总成绩：{} 班级排名：{}'.format(d[0], self.stu_name, d[1], rank))
                                no_study_record = False
                            rank += 1
                        if no_study_record:
                            print('你还未交过作业！无成绩！')
                    else:
                        print('你不是此班级学员！')
                else:
                    print('班级不存在！')

            elif stu_choice == 'b':
                break
            elif stu_choice == 'q':
                print("\033[33;1m感谢使用学员管理系统。\033[0m")
                exit()
            else:
                print("\033[31;1m请输入正确的选项！\033[0m")

    def if_class_exist(self, class_name):
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()
        if class_obj:
            return class_obj
        else:
            return False