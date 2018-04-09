#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import getpass
f = open('accountfile', 'r+', encoding='utf-8')
while True:
    ask = input("你是老用户吗？Y or N :")
    if ask == 'N':
        print('现在注册个吧!')
        while   True:
            account = input('请输入你的用户名：')
            exist = False
            for line in f:
                if account in line:
                    print('你已经注册过了，请直接登录。')
                    exist = True
                    break
            if not exist:
                password = getpass.getpass('请输入你的密码：')
                password1 = getpass.getpass('请再次输入你的密码：')
                if password =='':
                    print('Error!密码不能为空')
                elif password == password1:
                    print('注册成功！')
                    f.write('%s:%s\n' %(account,password))
                    f.flush()
                    break
                else:
                    print('Error!两次密码不一致,请重新填写注册信息。')
            else:
                break
        break

    else:
        break
print('请输入账号密码进行登录')
account_l = input('账号：')
def if_exist():
    f = open('accountfile', 'r+', encoding='utf-8')
    f1 = open('lockfile', 'r', encoding='utf-8')
    for lock_line in f1:
        if account_l in lock_line:
            print('你的账号已被锁定，请联系管理员。')
            exit()
    for line1 in f:
        exist1 = False
        if  account_l in line1:
            exist1 = True
            return exist1
    f.close()
    f1.close()
a = if_exist()
if  not a:
    print('你的账户不存在，请到登录界面注册。')
    exit()
num = 0
f1 = open('lockfile', 'r+', encoding='utf-8')
while num < 3:
    password_l = input('密码：')
    # login = account_l+':'+password_l
    login = ':'.join([account_l,password_l])
    # login = '%s:%s' %(account_l,password_l)
    f = open('accountfile', 'r+', encoding='utf-8')
    for line2 in f:
        if login in line2:
            print('成功登录！！！')
            exit()
    num += 1
    print('密码错误，请重新输入。')
else:
    print('由于多次输入错误，您的账户已被锁定，请联系管理员。')
    f1.write('%s\n' %account_l)
f.close()
f1.close()