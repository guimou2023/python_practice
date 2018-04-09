#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import  os

# 创建数据存放文件夹
if not os.path.exists('db'):
    os.mkdir('db')
BASH_DIR = os.path.dirname(__file__)
DB_DIR= os.path.join(BASH_DIR,'db')
if not os.path.join(BASH_DIR,'db'):
    os.mkdir('db')

#商品列表
goods_list = [
        ("iphone", 18000),
        ("Macbook pro", 10000),
        ("Iwatch", 5000),
        ("bike", 2000)]

#展示商品列表函数
def good_list():
    print("所有商品清单如下：")
    for index, iterm in enumerate(goods_list):
        print(index, iterm)
    return ''
#展示帮助函数
def help_show():
    print("请根据如下提示输入：")
    print("h => 获取帮助；L => 获取商品列表；l => 已购商品列表；数字 => 购买对应商品；q => 结束购物")

#db数据读取函数
def db_read(username):
    username_path = os.path.join(DB_DIR,username)
    with open(username_path, 'r') as f:
        f1 = f.read()
    return eval(f1)

#登录校验函数
def login_analyse(username):
    username_path = os.path.join(DB_DIR,username)
    if os.path.exists(username_path):
        password = input('请输入登录密码：')
        data = db_read(username)
        if data['passwd'] == password:
            print('%s 你好! 欢迎登录' %username)
            print('购物车商品列表：',data['shopping_list'])
        else:
            print('密码输入有误，请重新登录！')
            exit()
    else:
        while True:
            print('你好 %s! 您是第一次登录，现在为您的账号设定密码吧。' %username)
            while True:
                password1 = input('登录密码：')
                password1 = password1.strip()
                password2 = input('再次输入登录密码：')
                password2 = password2.strip()
                if password1 == '':
                    print('Error!密码不能为空')
                    continue
                elif not password2 == password1:
                    print('两次密码输入不一致！请重新输入注册密码')
                elif password2 == password1:
                    print('注册成功！')
                    break
                else:
                    continue
            while True:
                salary = input('请输入你的工资：')
                if not salary.isdigit():
                 print('输入有误！')
                 continue
                else:
                    break
            new_user = {
                'passwd':password1,
                'balance':salary,
                'shopping_list':'[]'
            }
            with open(username_path,'w') as f:
                f.write(str(new_user))
                break

#商品购买函数
def good_buy(username):
    while True:
        data = db_read(username)
        balance = int(data['balance'])
        choice = input("请输入想要购买商品的编号：")
        username_path = os.path.join(DB_DIR, username)
        if choice.isdigit():
            choice=int(choice)
            if choice >= 0 and choice < len(goods_list):
                if goods_list[choice][1] <=  balance:
                    balance -= goods_list[choice][1]
                    shop_list = eval(str(data['shopping_list']))
                    shop_list.append(goods_list[choice])
                    update_user = {
                        'passwd': data['passwd'],
                        'balance': balance,
                        'shopping_list': shop_list
                    }
                    with open(username_path, 'w') as f:
                        f.write(str(update_user))
                    print("Add %s into shopping cart.The current account balance is \033[1;31m%s\033[0m." %(goods_list[choice], balance))
                else:
                    print("亲！你钱不够啦，就剩%s了，快去搬砖吧！键入 q 结束购物。" %balance)
            else:
                print("您选购的商品不存在")
        elif choice == 'L':
            good_list()
        elif choice == 'l':
            print(data['shopping_list'])
        elif choice == 'q':
            break
        elif choice == 'h':
            print(help_show())
        else:
            print(help_show())
    print("已购商品列表".center(50,"-") )
    data = db_read(username)
    print(data['shopping_list'])
    balance = data['balance']
    print('余额：\033[1;32m%s\033[0m' %balance)

username = input("请输入账号:")
login_analyse(username)
good_list()
good_buy(username)