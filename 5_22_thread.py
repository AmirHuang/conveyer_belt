# _*_ coding: utf-8 _*_
# @time     : 2019/05/22
# @Author   : Amir
# @Site     : 
# @File     : 5_22_thread.py
# @Software : PyCharm

import paramiko
import time
import threading, queue
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
        result = ssh_shell.recv(102400).decode()
        ssh.close()
        print('成功')
        return result
    except:
        print('Error')
        return 'Error'


def product(q, p):
    while q.empty():
        ip = q.get()
        result = ssh(ip, username, password, cmd)
        if result != 'Error':
            p.put(ip)
            conn.set(ip, result)
        time.sleep(2)
    # 任务完成
    # p.task_done()


def custom(p):
    while p.empty():
        ip = p.get()
        result = conn.get(ip)
        print(result)
        time.sleep(2)
    # 任务完成
    # p.task_done()


if __name__ == '__main__':

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    conn = redis.Redis(connection_pool=pool)
    # pi = conn.pipeline()
    cmd = ['ls /bin -a', 'ifconfig']
    username = 'root'
    password = '123456'
    # ip = '192.168.58.128'
    q = queue.Queue()
    p = queue.Queue()
    for i in range(100):
        ip = '192.168.58.128'
        q.put(ip)

    # 启动生产者
    for i in range(4):
        threading.Thread(target=product, args=(q, p)).start()
    time.sleep(10)
    # 启动消费者
    for i in range(3):
        threading.Thread(target=custom, args=(p,)).start()
