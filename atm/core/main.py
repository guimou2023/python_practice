#!_*_coding:utf-8_*_
#__author__:"HOWard"

'''
main program handle module , handle all the user interaction stuff

'''

from core import auth,logger,accounts,transaction,db_handler,manage
from core.auth import login_required
from core import shopping as shop
from conf import settings
import time

#transaction logger
trans_logger = logger.logger('transaction')
#access logger
access_logger = logger.logger('access')

#temp account data ,only saves the data in memory
user_data = {
    'account_id':None,
    'is_authenticated':False,
    'account_data':None

}

def account_info(acc_data):
    user_data = db_handler.file_execute('select_course_system * from accounts where account=%s' % acc_data['account_id'])
    print('\033[1;33m%s\033[0m' %user_data)

@login_required
def repay(acc_data):
    '''
    print current balance and let user repay the bill
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    #for k,v in account_data.items():
    #    print(k,v )
    current_balance= ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
        if len(repay_amount) >0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' %(new_balance['balance']))
                break

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)

        if repay_amount == 'b':
            back_flag = True

@login_required
def withdraw(acc_data):
    '''
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance= ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if len(withdraw_amount) >0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' %(new_balance['balance']))
                break

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)

        if withdraw_amount == 'b':
            back_flag = True
@login_required
def shopping(acc_data):
    shop.login_init(acc_data)
    shop.good_buy(acc_data)

@login_required
def transfer(acc_data):
    A_id = acc_data['account_id']
    A_account_data = accounts.load_current_balance(A_id)
    B_id = input('请输入转入账号：').strip()
    B_account_data = accounts.load_current_balance(B_id)
    trans_amount = int(input('请输入转账金额：').strip())

    transaction.make_transaction(trans_logger, A_account_data, 'transferred-out',trans_amount)
    logger.logger('bills', A_account_data['id'], '转账','转出：%s' % trans_amount)

    transaction.make_transaction(trans_logger, B_account_data,'transferred-in',trans_amount)
    logger.logger('bills', B_account_data['id'], '转账','转入：%s' % trans_amount)

    print('\033[1;32m转账成功\033[0m')

@login_required
def pay_check(acc_data):
    load_dir = '%s/log/bills/%s_bill.log' %(settings.BASE_DIR,acc_data['account_id'])
    with open(load_dir,'r',encoding='utf-8') as f:
        for i in f:
            print('\033[1;33m%s\033[0m' %i.strip())

def logout(acc_data):
    logger.logger('login', acc_data['account_id'], '登出', '普通用户 [%s] 登出成功。' % acc_data['account_id'])
    exit('bye!')
def interactive(acc_data):
    '''
    interact with user
    :return:
    '''
    menu = u'''
  \033[1;31m------- ATM Bank ---------\033[0m
    \033[32;1m
    1.  账户信息查询
    2.  购物
    3.  还款
    4.  取款
    5.  转账
    6.  账单
    7.  退出
    \033[0m'''
    menu_dic = {
        '1': account_info,
        '2': shopping,
        '3': repay,
        '4': withdraw,
        '5': transfer,
        '6': pay_check,
        '7': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            # print('accdata',acc_data)
            #acc_data['is_authenticated'] = False
            menu_dic[user_option](acc_data)

        else:
            print("\033[31;1mOption does not exist!\033[0m")
def run():
    '''
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    '''
    acc_data = auth.acc_login(user_data,access_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        if user_data['account_data']['status'] == 3:
            logger.logger('login', acc_data['id'], '登录', '管理员 [%s] 登录成功。' %acc_data['id'])
            manage.admin(acc_data['id'])
        else:
            logger.logger('login', acc_data['id'], '登录', '普通用户 [%s] 登录成功。' %acc_data['id'])
            interactive(user_data)
