# _*_ coding: utf-8 _*_
# @time     : 2019/05/23
# @Author   : Amir
# @Site     : 
# @File     : 5_23_共享变量_互斥锁.py
# @Software : PyCharm

import paramiko
import time
import threading, queue
import redis
import random
import threading
import time

url_lists = []


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


def get_urls():
    # 模拟爬取url
    global url_lists
    ip_list = []
    for i in range(10):
        ip_list.append('192.168.58.128')
    for ip in ip_list:
        result = ssh(ip, username, password, cmd)
        import uuid
        xx = uuid.uuid4()
        conn.set(xx, result)
        url_lists.append(xx)


def get_detail():
    # 模拟爬取页面内容
    global url_lists
    if len(url_lists):
        xx = url_lists.pop()
        result = conn.get(xx)
        print(result)
        time.sleep(3)


if __name__ == '__main__':
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    conn = redis.Redis(connection_pool=pool)
    # pi = conn.pipeline()
    cmd = ['ls /bin -a', 'ifconfig']
    username = 'root'
    password = '123456'
    # ip = '192.168.58.128'
    # 爬取url链接
    for i in range(3):
        thread_get_urls = threading.Thread(target=get_urls)
        thread_get_urls.start()
    time.sleep(3)
    t = threading.Thread(target=get_detail)
    t.start()
    # thread_get_urls.join()
    # t.join()