# _*_ coding: utf-8 _*_
# @time     : 2019/05/23
# @Author   : Amir
# @Site     : 
# @File     : 5_23生产_消费.py
# @Software : PyCharm


from queue import Queue  # Queue在3.x中改成了queue
import random
import threading
import time
import paramiko
import time
import threading, queue
import redis
import random
import threading
import time


class Producer(threading.Thread):
    """
    Producer thread 制作线程
    """

    def __init__(self, queue):  # 传入线程名、实例化队列
        threading.Thread.__init__(self)  # t_name即是threadName
        self.data = queue

    """
    run方法 和start方法:
    它们都是从Thread继承而来的，run()方法将在线程开启后执行，
    可以把相关的逻辑写到run方法中（通常把run方法称为活动[Activity]）；
    start()方法用于启动线程。
    """

    def run(self):
        ip_list = []
        for i in range(10):
            ip_list.append('192.168.58.128')
        for ip in ip_list:
            result = ssh(ip, username, password, cmd)
            import uuid
            uid = uuid.uuid4()
            conn.set(uid, result)
            self.data.put(uid)


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


class Consumer(threading.Thread):
    """
    Consumer thread 消费线程，感觉来源于COOKBOOK
    """

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.data = queue

    def run(self):
        print(self.data.empty())
        while not self.data.empty():
        # if not self.data.empty():
            uid = self.data.get()
            result = conn.get(uid)
            print(result)
            time.sleep(5)


def main():
    """
    Main thread 主线程
    """
    queue = Queue()  # 队列实例化
    producer = Producer(queue)  # 调用对象，并传如参数线程名、实例化队列
    consumer = Consumer(queue)  # 同上，在制造的同时进行消费
    producer.start()  # 开始制造
    time.sleep(9)
    consumer.start()  # 开始消费
    """
    join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
　　join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
    """
    producer.join()
    consumer.join()
    print('All threads terminate!')


if __name__ == '__main__':
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    conn = redis.Redis(connection_pool=pool)
    # pi = conn.pipeline()
    cmd = ['ls /bin -a', 'ifconfig']
    username = 'root'
    password = '123456'
    # ip = '192.168.58.128'
    main()
