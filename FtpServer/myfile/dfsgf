# -*- coding: utf-8 -*-
# @Time    : 19-2-21 下午2:32
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : thread_1.py
# @Software: PyCharm

import threading
from time import sleep, time
import os

start = time()
a = 1

# 线程函数
def music():
    global a
    print('a =', a)
    a = 10000
    for i in range(5):
        sleep(2)
        print('播放学猫叫...', os.getpid())

# 创建线程对象
t = threading.Thread(target=music)
t.start()

# 主线程运行任务
for i in range(3):
    sleep(3)
    print('播放我的卡路里', os.getpid())

print('')
t.join()

print('Main thread', a)
print(time() - start)