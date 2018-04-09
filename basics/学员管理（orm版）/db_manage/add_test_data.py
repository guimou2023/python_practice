#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
from core import init_db
from sqlalchemy.orm import sessionmaker


stu_obj1 = init_db.Student(stu_name='小明', qq='111')
stu_obj2 = init_db.Student(stu_name='小米', qq='222')
stu_obj3 = init_db.Student(stu_name='小王', qq='333')

class_obj1 = init_db.Class(class_name='python 1班', course_name='python')
class_obj2 = init_db.Class(class_name='linux 1班', course_name='linux')


teacher_obj1 = init_db.Teacher(teacher_name='Alex')
teacher_obj2 = init_db.Teacher(teacher_name='Wu')

class_obj1.teachers = [teacher_obj1, teacher_obj2]
class_obj2.teachers = [teacher_obj1, teacher_obj2]

class_obj1.students = [stu_obj1, stu_obj2]
class_obj2.students = [stu_obj3]

course_obj1 = init_db.Course(content='python现状')
class_m2m_course__obj = init_db.Class_m2m_course(class_id=1, day_id=1, course_id=1)
session = sessionmaker(init_db.engine)()
session.add_all([class_obj1, class_obj2, course_obj1,class_m2m_course__obj,])
session.commit()




