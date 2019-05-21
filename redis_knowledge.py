# _*_ coding: utf-8 _*_
# @time     : 2019/05/21
# @Author   : Amir
# @Site     : 
# @File     : redis_knowledge.py
# @Software : PyCharm


import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)

r = redis.Redis(connection_pool=pool)
a = [1, 2, 3]
r.set('key1', str(a))

b = r.get('key1')

print(b.decode())
print(a)
print(type(b.decode()))
if eval(b.decode()) == a:
    print(True)
else:
    print(False)