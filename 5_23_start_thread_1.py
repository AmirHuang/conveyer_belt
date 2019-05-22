# _*_ coding: utf-8 _*_
# @time     : 2019/05/23
# @Author   : Amir
# @Site     : 
# @File     : 5_23_start_thread_1.py
# @Software : PyCharm

import threading
import paramiko
import time


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


if __name__ == '__main__':
    cmd = ['ls /bin -a', 'ls /bin -a']
    username = 'root'
    password = '123456'
    ip = '192.168.58.128'
    for i in range(5):
        t = threading.Thread(target=ssh, args=(ip, username, password, cmd))
        print(threading.current_thread().name)
        t.start()
        # t.join()