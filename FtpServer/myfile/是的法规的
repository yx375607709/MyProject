# -*- coding: utf-8 -*-
# @Time    : 19-2-21 下午5:16
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : thread_event.py
# @Software: PyCharm

from threading import Thread, Event

FLAG = None         # 全局变量用于通信
e = Event()

def fun():
    print('Fun 前来拜山头...')
    global FLAG
    FLAG = '天王盖地虎'
    e.set()

t = Thread(target=fun)
t.start()

# 主线程验证口令
print('说对口令就是自己人')

e.wait()    # 添加阻塞

if FLAG == '天王盖地虎':
    print('确认过眼神,你是对的人...')
else:
    print('打死他...')

t.join()

