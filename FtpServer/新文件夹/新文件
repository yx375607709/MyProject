# -*- coding: utf-8 -*-
# @Time    : 19-2-21 下午3:28
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : thread_3.py
# @Software: PyCharm


from threading import Thread
from time import sleep, time

start = time()

def fun():
    sleep(2)
    print('线程属性测试...')

t = Thread(target=fun, name='Tarena')
# 线程名称
print('Thread name', t.name)
t.setName('Tedu')

print('Thread name', t.getName())

# 设置主线程结束,分支结束
t.setDaemon(True)

t.start()
# 线程是否在生命周期
print('alive :', t.is_alive())

t.join()