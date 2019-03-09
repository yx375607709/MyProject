# -*- coding: utf-8 -*-
# @Time    : 19-2-21 上午9:50
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : value.py.py
# @Software: PyCharm

from multiprocessing import Value, Process
from time import sleep
import random

# 创建共享空间
money = Value('i', 5000)

# 操作共享空间
def man():  # 挣钱
    for _ in range(30):
        sleep(0.2)
        money.value += random.randint(1, 1000)

def girl(): # 花钱
    for _ in range(30):
        sleep(0.3)
        money.value -= random.randint(100, 900)

p1 = Process(target=man)
p2 = Process(target=girl)

p1.start()
p2.start()
p1.join()
p2.join()

print('一月余额: {}'.format(money.value))
