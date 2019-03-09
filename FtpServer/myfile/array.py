# -*- coding: utf-8 -*-
# @Time    : 19-2-21 上午10:17
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : array.py
# @Software: PyCharm

from multiprocessing import Array, Process
from time import sleep

# 创建共享内存:
# shm = Array('i', [1, 2, 3, 4, 5])

# 创建共享内存,指定开辟空间大小
# shm = Array('i', 6)

# 创建共享空间,存入字符串
shm = Array('c', b'Hello')

def fun():
    for i in shm:
        print(i, end=' ')
    shm[3] = b'3'
    print()

p = Process(target=fun)
p.start()
p.join()

for i in shm:
    print(i, end=' ')
print()
print(shm.value)    # 如果参数类型是字符串,得到 "b'Hel3o'"