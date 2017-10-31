#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import pickle,os
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)),'db')
STU_DB = os.path.join(BASE_DIR,'students_db')

# 创建学校
def init():
    school_info = {'1':'shanghai','2':'beijing'}
    with open(os.path.join(BASE_DIR,'school_info'), 'wb') as fs:
        pickle.dump(school_info,fs)

class   Show(object):

    @staticmethod
    def show_class_info():
        if  os.path.exists(os.path.join(BASE_DIR, 'class_info')):
            with open(os.path.join(BASE_DIR, 'class_info'), 'rb') as fc:
                show_data = pickle.load(fc)
                print('班级信息：')
                for i in show_data:
                   print('%s.%s' %(i,show_data[i]['class_name']))
                return show_data[i]['teacher_id']
        else:
            print('无班级信息，请联系管理员创建班级！')
            return False
    @staticmethod
    def show_classmates_info(teacher_id):
        if os.path.exists(os.path.join(BASE_DIR, 'teacher_info')):
            with open(os.path.join(BASE_DIR,'teacher_info'),'rb') as ft:
                show_data = pickle.load(ft)
            if teacher_id in show_data.keys():
                stu_id_data = show_data[teacher_id]['students_total']
                print('学员列表：')
                for i in stu_id_data:
                    stu_path = '%s/%s' %(STU_DB,i)
                    with open(stu_path,'rb') as f:
                        data = pickle.load(f)
                    print('%s. %s' %(i,data['name']))
    @staticmethod
    def if_teacher_id_exist(teacher_id):
        if os.path.exists(os.path.join(BASE_DIR, 'teacher_info')):
            with open(os.path.join(BASE_DIR,'teacher_info'),'rb') as ft:
                show_data = pickle.load(ft)
            if teacher_id in show_data.keys():
                return True
            else:return False
    @staticmethod
    def show_class_name(class_id):
        if os.path.exists(os.path.join(BASE_DIR, 'class_info')):
            with open(os.path.join(BASE_DIR,'class_info'),'rb') as ft:
                show_data = pickle.load(ft)
                return show_data[class_id]['class_name']

class   Create(object):

    @staticmethod
    def create_teacher():
        teacher_info = {'name': None, 'sex': None, 'students_total': []}
        name = input('教师姓名:')
        sex = input('教师性别:')
        teacher_info['name'] = name
        teacher_info['sex'] = sex
        if  os.path.exists(os.path.join(BASE_DIR,'teacher_info')):
            with open(os.path.join(BASE_DIR,'teacher_info'),'rb') as ft:
                data = pickle.load(ft)
            for i in data:
                if data[i]['name'] == name.strip():
                    print('该教师已经注册了哦，请重试！')
                    continue
            num = 1
            while str(num) in data.keys():
                num += 1
            # print('num',num)
            data[str(num)] = teacher_info
            # print('data',data)
            with open(os.path.join(BASE_DIR, 'teacher_info'), 'wb') as ft:
                pickle.dump(data,ft)
        else:
            dump_data = {}
            dump_data['1'] = teacher_info
            with open(os.path.join(BASE_DIR, 'teacher_info'), 'wb') as ft:
                pickle.dump(dump_data,ft)
    @staticmethod
    def create_course():
        course_info = {'course_name': None, 'period': None, 'price': None, 'school_id': None}
        course_name = input('课程名:').strip()
        period = input('培训周期:').strip()
        price = input('课程学费:').strip()
        course_info['course_name'] = course_name
        course_info['period'] = period
        course_info['price'] = price
        print('选择校区: 1.上海 2.北京 (输入对应数字)')
        while True:
            chocie = input('>>:').strip()

            if chocie.isdigit():
                break
            else:
                print('请输入对应数字！')
        course_info['school_id'] = chocie
        if  os.path.exists(os.path.join(BASE_DIR,'course_info')):
            with open(os.path.join(BASE_DIR,'course_info'),'rb') as fc:
                data = pickle.load(fc)
            for i in data:
                if data[i]['course_name'] == course_name.strip():
                    print('该课程已经存在了哦，请重试！')
                    break
            else:
                num = 1
                while str(num) in data.keys():
                    num += 1
                data[str(num)] = course_info
                with open(os.path.join(BASE_DIR, 'course_info'), 'wb') as fc:
                    pickle.dump(data,fc)
        else:
            dump_data = dict()
            dump_data['1'] = course_info
            with open(os.path.join(BASE_DIR, 'course_info'), 'wb') as fc:
                pickle.dump(dump_data,fc)

    @staticmethod
    def create_class():
        if not os.path.exists(os.path.join(BASE_DIR, 'course_info')):
            exit('没有可绑定的课程，请先去创建课程')
        if not os.path.exists(os.path.join(BASE_DIR, 'teacher_info')):
            exit('无讲师信息，请先去录入讲师信息！')
        class_name = input('班级名>>:').strip()
        if class_name == '':
            pass
        else:
            if os.path.exists(os.path.join(BASE_DIR, 'class_info')):
                with open(os.path.join(BASE_DIR, 'class_info'), 'rb') as fc:
                    data = pickle.load(fc)
                for i in data:
                    if data[i]['class_name'] == class_name.strip():
                        exit('该班级已经存在了哦，请重试！')
            with open(os.path.join(BASE_DIR, 'course_info'), 'rb') as fc:
                course_data = pickle.load(fc)
            print('请输入想绑定的课程对应的编号！')
            print('课程列表：')
            for i in course_data:
                print('%s.%s' %(i,course_data[i]['course_name']))
            while True:
                course_id = input('>>:').strip()
                if  course_id.isdigit():
                    break
                else:
                    print('请输入对应数字！')
            with open(os.path.join(BASE_DIR, 'teacher_info'), 'rb') as ft:
                teacher_data = pickle.load(ft)
            print('请输入想绑定的讲师对应的编号！')
            print('讲师列表：')
            for i in teacher_data:
                print('%s.%s' %(i,teacher_data[i]['name']))
            while True:
                teacher_id = input('>>:').strip()
                if teacher_id.isdigit():
                    break
                else:
                    print('请输入对应数字！')
            class_info = {'class_name':class_name,'course_id':course_id,'teacher_id':teacher_id}
            if  os.path.exists(os.path.join(BASE_DIR,'class_info')):
                with open(os.path.join(BASE_DIR,'class_info'),'rb') as fc1:
                    data = pickle.load(fc1)
                num = 1
                while str(num) in data.keys():
                    num += 1
                data[str(num)] = class_info
                with open(os.path.join(BASE_DIR, 'class_info'), 'wb') as fc2:
                    pickle.dump(data,fc2)
            else:
                dump_data = dict()
                dump_data['1'] = class_info
                with open(os.path.join(BASE_DIR, 'class_info'), 'wb') as fc:
                    pickle.dump(dump_data,fc)

    @staticmethod
    def create_student():
        stu_file_list = os.listdir(STU_DB)
        num = 1
        file_name = 'stu1'
        while file_name in  stu_file_list:
            num += 1
            file_name = 'stu%s' %num
        else:
            new_stu_path = '%s/%s' %(STU_DB,file_name)
            name = input('姓名:').strip()
            sex = input('性别:').strip()
            balance = input('预交学费:').strip()
            res = Show.show_class_info()
            if res:
                with open(os.path.join(BASE_DIR, 'class_info'), 'rb') as fc:
                    class_data = pickle.load(fc)
                while True:
                    choice = input('输入对应班级数字:')
                    if choice.isdigit():
                        break

                teacher_id = class_data[str(choice)]['teacher_id']
                new_stu_data = dict()
                new_stu_data['name'] = name
                new_stu_data['sex'] = sex
                new_stu_data['balance'] = balance
                new_stu_data['teacher_id'] = teacher_id
                new_stu_data['score'] = 0
                new_stu_data['class_id'] = choice
                with open (new_stu_path,'wb') as f:
                    pickle.dump(new_stu_data,f)
                with open(os.path.join(BASE_DIR, 'teacher_info'), 'rb') as ft:
                    teacher_data = pickle.load(ft)
                teacher_data[teacher_id]['students_total'].append(file_name)
                with open(os.path.join(BASE_DIR, 'teacher_info'), 'wb') as ft:
                    pickle.dump(teacher_data,ft)
                print('注册成功！')
                print('您的学员ID：%s（此ID为查询个人信息的唯一标识，请牢记！）' %file_name)

class Manage(object):
    @staticmethod
    def score_management(stu_file_name):
        load_file_path = '%s/%s' %(STU_DB,stu_file_name)
        with open(load_file_path,'rb') as f1:
            stu_data = pickle.load(f1)
            name = stu_data['name']
            score = stu_data['score']
        print('%s的当前分数为%d' %(name,score))
        stu_data['score'] = int(input('将其分数修改为>>:').strip())
        with open(load_file_path, 'wb') as f2:
            pickle.dump(stu_data,f2)

class   View(object):

    @staticmethod
    def stu_view():
        print('\033[1;33mWelcome to login student terminal！\033[0m')
        notice_info = '''\033[1;34m
            1.学员注册
            2.查询个人信息
            3.退出\033[0m
        '''
        while True:
            print(notice_info)
            choice = input('>>:').strip()
            if choice == '1':
                Create.create_student()
            elif choice == '2':
                print('温馨提示：查询信息需提供学员id，学员id在注册成功时生成，如忘记请联系管理员查询！')
                stu_id = input('ID >>:').strip()
                query_file_path = '%s/%s' %(STU_DB,stu_id)
                with open(query_file_path,'rb') as qf:
                    data = pickle.load(qf)
                name = data['name']
                sex = data['sex']
                balance = data['balance']
                class_name = Show.show_class_name(data['class_id'])
                score = data['score']
                # print(type(name),type(sex),type(class_name),type(score))
                info = '''
                学员姓名:%s
                性别：%s
                账户余额：%s
                班级：%s
                成绩：%d
                      ''' %(name,sex,balance,class_name,score)
                print(info)
            elif choice == '3':
                break
            else:print('请输入选项对应的数字！')

    @staticmethod
    def teach_view():
        print('\033[1;33mWelcome to login teacher terminal！\033[0m')
        notice_info = '''\033[1;34m
                1.查看学员列表
                2.修改学员成绩
                3.退出\033[0m
                '''
        while True:
            print('请输入教师id，如1、2、3 !')
            teacher_id = input('>>:').strip()
            if not Show.if_teacher_id_exist(teacher_id):
                print('该讲师不存在')
                continue
            else:break
        while True:
            print(notice_info)
            choice = input('>>:').strip()
            if choice == '1':
                Show.show_classmates_info(teacher_id)
            elif choice == '2':
                print('请输入学生id，如stu1、stu2 !')
                stu_file_name = input('>>:').strip()
                Manage.score_management(stu_file_name)
                print('修改成功！')
            elif choice == '3':break
            else:print('请输入对应数字')
    @staticmethod
    def admin_view():
        print('\033[1;33mWelcome to login manage terminal！\033[0m')
        notice_info = '''\033[1;34m
        1.创建讲师
        2.查询班级信息
        3.创建课程
        4.创建班级
        5.退出\033[0m
        '''
        while True:
            print(notice_info)
            choice = input('>>:').strip()
            if choice == '1':Create.create_teacher()
            elif choice == '2':Show.show_class_info()
            elif choice == '3':Create.create_course()
            elif choice == '4':Create.create_class()
            elif choice == '5':break
            else:print('请输入对应数字')
def run():
    init()
    print('\033[1;33m欢迎登录选课系统！\033[0m'.center(31,'*'))
    while True:
        print('''\033[1;34m
        1.学员视图
        2.讲师视图
        3.管理视图
        4.退出\033[0m''')
        rec = input('>>:')
        if rec == '4':
            exit('bye!')
        elif rec == '1':
            View.stu_view()
        elif rec == '2':
            View.teach_view()
        elif rec == '3':
            View.admin_view()
        else:print('请输出功能对应的数字！')


# with open(os.path.join(BASE_DIR, 'class_info'), 'rb') as fc:
#     data = pickle.load(fc)
#     print(data)
run()
