#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import  os,logging
from core import transaction,logger,accounts

trans_logger = logger.logger('transaction')

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
        print('\033[32;1m%s,%s\033[0m' %(index, iterm))
    return ''
#展示帮助函数
def help_show():
    print("\033[1;33m请根据如下提示输入：\nh => 获取帮助；L => 获取商品列表；l => 已购商品列表；数字 => 购买对应商品；q => 结束购物；p => 调用ATM结账\033[0m")
    return ''

#db数据读取函数
def db_read(username):
    BASH_DIR = os.path.dirname(os.path.dirname(__file__))
    DB_DIR = os.path.join(BASH_DIR, 'db/order_info')
    username_path = os.path.join(DB_DIR,username)
    with open(username_path, 'r') as f:
        f1 = f.read()
    return eval(f1)

#登录初始化
def login_init(accdata):
    BASH_DIR = os.path.dirname(os.path.dirname(__file__))
    DB_DIR= os.path.join(BASH_DIR,'db/order_info')
    username = accdata['account_id']
    username_path = os.path.join(DB_DIR,username)
    if os.path.exists(username_path):
        data = db_read(username)
        print('\033[1;30m%s 你好! 欢迎登录商城\033[0m' %username)
        help_show()
        if not data['shopping_list'] == '[]':
            print('您的购物车商品列表：',data['shopping_list'])

    else:
        print('你好 %s! 你的购物车是空的哦，快去抢购吧。' %username)
        help_show()
        salary = accdata['account_data']['balance']
        new_user = {
            'balance':salary,
            'shopping_list':'[]',
            'need_paid':0
        }
        with open(username_path,'w') as f:
            f.write(str(new_user))

#商品购买函数
def good_buy(acc_data):
    BASH_DIR = os.path.dirname(os.path.dirname(__file__))
    order_info_dir = os.path.join(BASH_DIR, 'db/order_info')
    username = acc_data['account_id']
    user_order_info_dir = '%s/%s' %(order_info_dir,username)
    while True:
        data = db_read(user_order_info_dir)
        # shop_balance = acc_data['account_data']['balance']
        # data['balance'] = shop_balance
        shop_balance = data['balance']
        bill = data['need_paid']
        choice = input("\033[1;31mInput：\033[0m")
        if choice.isdigit():
            choice=int(choice)
            if choice >= 0 and choice < len(goods_list):
                if goods_list[choice][1] <= shop_balance:
                    shop_balance -= goods_list[choice][1]
                    bill += goods_list[choice][1]
                    shop_list = eval(str(data['shopping_list']))
                    shop_list.append(goods_list[choice])
                    update_user = {
                        'balance': shop_balance,
                        'shopping_list': shop_list,
                        'need_paid':bill
                    }
                    with open(user_order_info_dir, 'w') as f:
                        f.write(str(update_user))
                    print("Add %s into shopping cart.The current account balance is \033[1;31m%s\033[0m." %(goods_list[choice], shop_balance))
                else:
                    print("亲！你钱不够啦，就剩%s了，快去搬砖吧！键入 q 结束购物! 键入p 结账退出" %shop_balance)
            else:
                print("您选购的商品不存在")
        elif choice == 'L':
            good_list()
        elif choice == 'l':
            if not data['shopping_list'] == '[]':
                print('您的购物车商品列表：', data['shopping_list'])
            else:
                print('你好 %s! 你的购物车是空的哦，快去抢购吧。' % username)
        elif choice == 'q':
            break
        elif choice == 'p':
            account_data = accounts.load_current_balance(acc_data['account_id'])
            transaction.make_transaction(trans_logger,account_data,'consume',bill)
            logger.logger('bills',acc_data['account_id'],'商城购物结账','转出：%s' % bill)
            os.remove(user_order_info_dir)
            print('结账成功，bye!')
            break
        elif choice == 'h':
            print(help_show())
        else:
            print(help_show())


