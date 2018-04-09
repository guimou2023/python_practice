#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import os,shutil
print('欢迎进入工资管理系统')
def help_show():
    print("1.查询员工工资\n2.修改员工工资\n3.增加新员工记录\n4.退出")
    print("键入数字进入对应菜单,二级菜单下键入空值返回上一层菜单。")
while True:
    help_show()
    Num = input("Your input is：")
    if Num == '1':
        print('进入工资查询界面')
        while True:
            Name = input('你要查询的员工是：')
            with open('info.txt', 'r') as f1:
                f2 = f1.read()
                if not Name in f2:
                    print('该员工不存在')
                    continue
            if Name.strip() == '':
                break
            with open('info.txt','r') as f:
                for i in f:
                    if Name in i:
                        I = i.split()
                        salary = I[1]
                        print('%s的工资为：%s' %(Name,salary))
    elif Num == '2':
        print('进入工资修改界面')
        while True:
            Name = input('你要修改工资的员工是：')
            with open('info.txt', 'r') as f1:
                f2 = f1.read()
                if not Name in f2:
                    print('该员工不存在')
                    continue
            if Name.strip() == '':
                break
            salary = input('想修改成：')
            if Name.strip() == '':
                break
            f = open('info.txt', 'r')
            f1 = open('info_update','w')
            for i in f:
                if Name in i:
                    i = '%s %s\n' %(Name,salary)
                f1.write(i)
            BASE_DIR = os.path.dirname(__file__)
            f.close()
            f1.close()
            shutil.copy('info_update','info.txt')
    elif Num == '3':
        print('进入增加新纪录界面')
        while True:
            Name = input('新员工名字：')
            if Name.strip() == '':
                break
            salary = input('新员工薪水：')
            if Name.strip() == '':
                break
            with open('info.txt', 'a') as f:
                i = '\n%s %s' % (Name,salary)
                f.write(i)
    elif Num == '4':
        exit()
    elif Num.strip() == '':
        exit()