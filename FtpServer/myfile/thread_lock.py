# -*- coding: utf-8 -*-
# @Time    : 19-2-21 下午5:37
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : lock.py.py
# @Software: PyCharm

from threading import Lock, Thread

a = b = 0

lock = Lock()   # 锁对象

def value():
    while True:
        lock.acquire()      # 上锁
        if a != b:
            print('a = {}, b = {}'.format(a, b))
        lock.release()      # 解锁

t = Thread(target=value)

t.start()

while True:
    with lock:      # 上锁,运行完后解锁
        a += 1
        b += 1

t.join()