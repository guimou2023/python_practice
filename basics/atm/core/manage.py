import os,json
from conf import settings
from core import logger
def admin(admin_id):
    print('Welcome! managers')
    choice = 0
    while  choice != '5':
        print()
        menu = '''
          \033[1;31m------- Account management interface ---------\033[0m
            \033[32;1m
                        1.  创建账户
                        2.  冻结账户
                        3.  解冻账户
                        4.  删除账户
                        5.  退出
            \033[0m'''
        print(menu)
        choice = input('\033[1;34minput：\033[0m').strip()
        if choice == '1':
            create_user()
            continue
        elif choice == '2':
            lock_user()
        elif choice == '3':
            un_lock_user()
        elif choice == '4':
            del_user()
    else:
        logger.logger('login', admin_id, '登出', '管理员 [%s] 登出成功。' % admin_id)
        print('bye!')

def create_user():
    account = input('设置新用户账户名：').strip()
    account_file = "%s/db/accounts/%s.json" % (settings.BASE_DIR, account)
    example_account_file = "%s/db/accounts/examples.json" % settings.BASE_DIR
    if os.path.isfile(account_file):
        print('error,账户已存在')
    else:
        with open(example_account_file, 'r') as f:
            account_data = json.load(f)
        credit = input('设置新账户额度：').strip()
        if not credit.isdigit():
            print('输入错误,额度必须为数字！')
            return
        account_data['balance'] = int(credit)
        account_data['credit'] =  account_data['balance']
        account_data['id'] = account
        account_data['password'] = input('设置新账户密码：').strip()
        with open(account_file, 'w') as f1:
            f1.write(json.dumps(account_data))
        if os.path.isfile(account_file):
            print('新用户创建成功')
        else:
            print('error！')


def del_user():
    account = input('待删除用户账户名：').strip()
    account_file = "%s/db/accounts/%s.json" % (settings.BASE_DIR, account)
    if os.path.isfile(account_file):
        os.remove(account_file)
        print('用户删除成功！')
    else:
        print('输入错误，该用户不存在。')
def lock_user():
    account = input('待锁定用户账户名：').strip()
    account_file = "%s/db/accounts/%s.json" % (settings.BASE_DIR, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            account_data['status'] = 1
        with open(account_file, 'w') as f1:
            f1.write(json.dumps(account_data))
        print('用户冻结成功！')
    else:
        print('输入错误，该用户不存在。')
def un_lock_user():
    account = input('待解冻用户账户名：').strip()
    account_file = "%s/db/accounts/%s.json" % (settings.BASE_DIR, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            account_data['status'] = 0
        with open(account_file, 'w') as f1:
            f1.write(json.dumps(account_data))
        print('用户解冻成功！')
    else:
        print('输入错误，该用户不存在。')
