#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import os,json,re

# 取数据库路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR,'db')
DB_FILE = os.path.join(DB_DIR,'form_info')

# 读取json数据到字典
f = open(DB_FILE,'r',encoding='utf-8')
data = json.loads(f.read())
f.close()

SQL = input('请输入sql语句:')

# 查询操作判断
RE = re.search('^\s*select_course_system\s+name,age\s+from\s+staff_table\s+where\s+age\s+>\s+(\d+)\s*$',SQL)
RE1 = re.search("^\S*select_course_system\s+[*]\s+from\s+staff_table\s+where\s+dept\s*=\s*'?\"?(\w+)'?\"?\s*$",SQL)
RE3 = re.search("^\s*select_course_system\s+[*]\s+from\s+staff_table\s+where\s+enroll_date\s+like\s+'?\"?(\w+)'?\"?\s*$",SQL)
# 插入操作判断
RE4 = re.search("^\s*insert\s+into\s+staff_table\(\s*name\s*,\s*age\s*,\s*phone\s*,\s*dept\s*,\s*enroll_date\s*\)\s+values\(\s*'?([^']+)'?\s*,\s*'?([^']+)'?\s*,\s*'?([^']+)'?\s*,\s*'?([^']+)'?\s*,\s*'?([^']+)'?\s*\)$",SQL)
# 删除操作判断
RE5 = re.search('^\s*([0-9]+)\s*$',SQL)
# 修改操作判断
RE6 = re.search("^\s*UPDATE\s+staff_table\s+SET\s+dept\s*=\s*\"?\'?(\w+)\'?\"?\s+WHERE\s+dept\s*=\s*\"?'?(\w+)'?\"?\s*$",SQL)

# 数据库处理
if RE:
    print('+' + '-'*10 + '+' + '-'*6 + '+')
    print('|' + 'NAME'.ljust(10) + '|' + 'AGE'.ljust(6) + '|')
    print('+' + '-' * 10 + '+' + '-' * 6 + '+')
    count = 0
    for i in data.keys():
        if int(data[i][1]) >  int(RE.groups()[-1]):
            count += 1
            print('|' + str(data[i][0]).ljust(10) + '|' + str(data[i][1]).ljust(6) + '|')
            print('+' + '-' * 10 + '+' + '-' * 6 + '+')
    else:
        print('%d row(s) returned' %count)

if RE1:
    print('+' + '-'*10 + '+' + '-'*10 + '+' + '-'*5 + '+' + '-'*15 + '+' + '-'*10 + '+' + '—'*13 + '+')
    print('|' + 'staff_id'.ljust(10) + '|' + 'name'.ljust(10) + '|' + 'age'.ljust(5) + '|' + 'phone'.ljust(15) + '|' + 'dept'.ljust(10) + '|' + 'enroll_date'.ljust(13) +   '|')
    print('+' + '-'*10 + '+' + '-'*10 + '+' + '-'*5 + '+' + '-'*15 + '+' + '-'*10 + '+' + '—'*13 + '+')
    count = 0
    for i in data.keys():
         if data[i][3] == RE1.groups()[-1]:
             count += 1
             print('|' + i.ljust(10)  + '|' + str(data[i][0]).ljust(10) + '|' + str(data[i][1]).ljust(5) + '|' + str(data[i][2]).ljust(15) + '|' + str(data[i][3]).ljust(10) + '|' + str(data[i][4]).ljust(13) + '|')
             print('+' + '-'*10 + '+' + '-'*10 + '+' + '-'*5 + '+' + '-'*15 + '+' + '-'*10 + '+' + '—'*13 + '+')
    else:
        print('%d row(s) returned' % count)

if RE3:
    print('+' + '-' * 10 + '+' + '-' * 10 + '+' + '-' * 5 + '+' + '-' * 15 + '+' + '-' * 10 + '+' + '—' * 13 + '+')
    print('|' + 'staff_id'.ljust(10) + '|' + 'name'.ljust(10) + '|' + 'age'.ljust(5) + '|' + 'phone'.ljust(15) + '|' + 'dept'.ljust(10) + '|' + 'enroll_date'.ljust(13) + '|')
    print('+' + '-' * 10 + '+' + '-' * 10 + '+' + '-' * 5 + '+' + '-' * 15 + '+' + '-' * 10 + '+' + '—' * 13 + '+')
    count = 0
    for i in data.keys():
        if  RE3.groups()[-1] in data[i][4]:
            count += 1
            print('|' + i.ljust(10) + '|' + str(data[i][0]).ljust(10) + '|' + str(data[i][1]).ljust(5) + '|' + str(data[i][2]).ljust(15) + '|' + str(data[i][3]).ljust(10) + '|' + str(data[i][4]).ljust(13) + '|')
            print('+' + '-' * 10 + '+' + '-' * 10 + '+' + '-' * 5 + '+' + '-' * 15 + '+' + '-' * 10 + '+' + '—' * 13 + '+')
    else:
        print('%d row(s) returned' % count)

if RE4:
    for i in data.keys():
        if  RE4.groups()[2] == str(data[i][2]):
            print("Error Code: 1062. Duplicate entry '4' for key 'PRIMARY'")
            exit()
    id4 = 1
    while str(id4) in data.keys():
        id4 += 1
    data[id4]=[RE4.groups()[0],RE4.groups()[1],RE4.groups()[2],RE4.groups()[3],RE4.groups()[4]]
    f1 = open(DB_FILE, 'w', encoding='utf-8')
    f1.write(json.dumps(data))
    f1.close()
if RE5:
    id5 = RE5.group()
    data.pop(id5)
    f2 = open(DB_FILE, 'w', encoding='utf-8')
    f2.write(json.dumps(data))
    f2.close()
    print('staff_id 为 %s 员工信息删除成功！' %id5)
if RE6:
    after_update = RE6.groups()[0]
    before_update = RE6.groups()[1]
    for i in data.keys():
        if  data[i][3] == before_update:
            data[i][3] = after_update
    f3 = open(DB_FILE, 'w', encoding='utf-8')
    f3.write(json.dumps(data))
    f3.close()
    print('修改成功')
