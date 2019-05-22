# _*_ coding: utf-8 _*_
# @time     : 2019/05/23
# @Author   : Amir
# @Site     : 
# @File     : 5_23thread_lock.py
# @Software : PyCharm


import threading

lock = threading.Lock()

num = 0


def run(n):
    global num
    for i in range(1000000):
        # 锁
        lock.acquire()
        try:
            num += n
            num -= n
        # except:
        #     continue
        finally:
            lock.release()


if __name__ == '__main__':
    t1 = threading.Thread(target=run, args=(6,))
    t2 = threading.Thread(target=run, args=(9,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(num)
