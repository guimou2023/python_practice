__author__ = "Alex Li"


import redis
import time

pool = redis.ConnectionPool(host='192.168.16.96', port=6379,db=5)

r = redis.Redis(connection_pool=pool)

# pipe = r.pipeline(transaction=False)
pipe = r.pipeline(transaction=True)

r.brpoplpush('names','names2',timeout=30)
r.set('name7', 'wupeiqi')
#
# # time.sleep(50)
# r.set('role2', 'sb')
pipe.execute()