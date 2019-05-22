# _*_ coding: utf-8 _*_
# @time     : 2019/05/22
# @Author   : Amir
# @Site     : 
# @File     : 5_22ssh.py
# @Software : PyCharm

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
        result = ssh_shell.recv(102400).decode()
        ssh.close()
        print('成功')
        return result
    except:
        print('Error')
        return 'Error'


if __name__ == '__main__':
    import redis
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    conn = redis.Redis(connection_pool=pool)
    pi = conn.pipeline()
    cmd = ['ls /bin -a', 'ifconfig']
    username = 'root'
    password = '123456'
    ip = '192.168.58.128'
    n = 1
    for i in range(100):
        print(n)
        result = ssh(ip, username, password, cmd)
        print(result)
        p.set(str(n), result)
        n += 1
        p.execute()