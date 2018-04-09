__author__ = "Alex Li"

import pymysql

# 创建连接
conn = pymysql.connect(host='192.168.16.86', port=3306, user='root', passwd='alex3714', db='oldboydb')

# 创建游标
cursor = conn.cursor()

# 执行SQL，并返回收影响行数
# effect_row = cursor.execute("select * from student")
# print(cursor.fetchone())
# print(cursor.fetchone())
# print('-------')
# print(cursor.fetchall())

data = [
    ("N1_%s" %i, "2015-05-22",'M') for i in range(10000)
]

print("start creeat....")
cursor.executemany("insert into student (name,register_date,gender) values(%s,%s,%s)" ,data)

conn.commit()