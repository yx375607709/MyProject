# -*- coding: utf-8 -*-
# @Time    : 19-2-21 下午2:55
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : thread_2.py
# @Software: PyCharm

from threading import Thread
from time import sleep, time

start = time()

def fun(sec, name):
    print('线程函数传参...')
    sleep(sec)
    print('%s 线程执行完毕' % name)

threads = []

for i in range(10):
    t = Thread(target=fun, args=(20,), kwargs={'name':'T%d' % i})
    t.start()
    threads.append(t)

for i in threads:
    i.join()