# -*- coding: utf-8 -*-
# @Time    : 19-2-21 下午5:10
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : event_test.py
# @Software: PyCharm

from threading import Event

# 创建事件对象
e = Event()

e.set()     # 设置e

print('6666666666666')

e.clear()   # 设置e回到初始状态,阻塞

print(e.is_set())   # 判断是否设置e

e.wait(3)   # 阻塞等待

print('888888888888888')

