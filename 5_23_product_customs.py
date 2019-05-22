# _*_ coding: utf-8 _*_
# @time     : 2019/05/23
# @Author   : Amir
# @Site     : 
# @File     : 5_23_product_customs.py
# @Software : PyCharm


import threading, queue, random, time
import threading
import paramiko
import time
import redis


def ssh(ip, username, password, cmd):
    try:
        transport = paramiko.Transport((ip, 22))
        transport.connect(username=username, password=password)
        ssh = paramiko.SSHClient()
        ssh._transport = transport
        ssh_shell = ssh.invoke_shell()  # 使用invoke是为了执行多条命令
        # print(ssh_shell.recv(102400).decode())
        for m in cmd:
            res = ssh_shell.sendall(m + '\n')
            time.sleep(2)
        result = ssh_shell.recv(1024000).decode()
        ssh.close()
        print('成功')
        print(threading.current_thread().name)
        return result
    except:
        print('Error')
        return 'Error'


def product(ip, username, password, cmd, q):
    result = ssh(ip, username, password, cmd)
    conn.set(ip)
    # 任务完成
    q.task_done()


def custom(id, q):
    while True:
        item = q.get()
        if item is None:
            break
        print('消费者%d消费了%d' % (id, item))
        time.sleep(2)
    # 任务完成
    q.task_done()


if __name__ == '__main__':
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    conn = redis.Redis(connection_pool=pool)
    # p = conn.pipeline()
    cmd = ['ls /bin -a', 'ls /bin -a']
    username = 'root'
    password = '123456'
    ip = '192.168.58.128'
    # 消息队列
    q = queue.Queue()

    # 启动生产者
    for i in range(4):
        threading.Thread(target=product, args=(i, q)).start()

    # 启动消费者
    for i in range(3):
        threading.Thread(target=custom, args=(i, q)).start()