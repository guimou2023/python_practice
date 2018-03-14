#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
from conf.settings import engine


"""
初始化数据库
"""

Base = declarative_base(engine)


class_m2m_teacher = Table('class_m2m_teacher', Base.metadata,
                          Column('class_id', Integer, ForeignKey('class.id')),
                          Column('teacher_id', Integer, ForeignKey('teacher.id'))
                          )
class_m2m_student = Table('class_m2m_student', Base.metadata,
                          Column('class_id', Integer, ForeignKey('class.id')),
                          Column('stu_id', Integer, ForeignKey('student.id'))
                          )


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    stu_name = Column(String(32), nullable=None, unique=True)
    qq = Column(Integer)

    classes = relationship('Class', secondary=class_m2m_student, backref='students')

    def __repr__(self):
        return "id:{} name:{} qq:{}".format(self.id, self.stu_name, self.qq)


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    teacher_name = Column(String(32), nullable=None, unique=True)

    classes = relationship('Class', secondary=class_m2m_teacher, backref='teachers')

    def __repr__(self):
        return "id:{} teacher_name:{}".format(self.id,self.teacher_name)


class Class(Base):
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    class_name = Column(String(32), nullable=None)
    course_name = Column(String(32), nullable=None)

    def __repr__(self):
        return 'id:{} class_name:{} course_name:{}'.format(self.id, self.class_name, self.course_name)


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    content = Column(String(32), nullable=None, unique=True)


class Class_m2m_course(Base):
    __tablename__ = 'class_m2m_course'
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer,  ForeignKey('class.id'))
    day_id = Column(Integer, nullable=None)
    course_id = Column(Integer, ForeignKey('course.id'))

    class_rela = relationship("Class", backref='class_courses')
    course_rela = relationship("Course")

    __table_args__ = (UniqueConstraint(class_id, day_id, name='class_course'),)


class StudyRecord(Base):

    __tablename__ = 'study_record'
    id = Column(Integer, primary_key=True)
    class_m2m_course_id = Column(Integer, ForeignKey('class_m2m_course.id'))
    stu_id = Column(Integer, ForeignKey('student.id'))
    status = Column(String(32), nullable=None)
    score = Column(Integer)

    record1 = relationship('Class_m2m_course', backref='lesson_learn_record')
    record2 = relationship('Student', backref='stu_record')

Base.metadata.create_all()
