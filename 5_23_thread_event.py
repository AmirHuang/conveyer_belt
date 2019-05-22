# _*_ coding: utf-8 _*_
# @time     : 2019/05/23
# @Author   : Amir
# @Site     : 
# @File     : 5_23_thread_event.py
# @Software : PyCharm


import threading, queue, random, time


def product(id, q):
    while True:
        num = random.randint(0, 10000)
        q.put(num)
        print('生产者%d生产了%d' % (id, num))
        time.sleep(3)
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
    # 消息队列
    q = queue.Queue()

    # 启动生产者
    for i in range(4):
        threading.Thread(target=product, args=(i, q)).start()

    # 启动消费者
    for i in range(3):
        threading.Thread(target=custom, args=(i, q)).start()