# !/usr/bin/python3
# coding=utf-8
# @Time    : 19-3-5 下午7:11
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : aaa.py
# @Software: PyCharm

import random

# 描述:
# 重复走访所有要排序的数据,依次比较每两个相邻的元素,如果两者次
# 序错误则交换,重复上面的过程,直到没有相邻数据需要交换为止,此时完成排序

count = 1
def fun(lst):
    global count
    FLAG = True
    for i in range(len(lst) - 1):
        num1 = lst[i]
        num2 = lst[i + 1]
        if num1 > num2:
            FLAG = False
            lst[i], lst[i + 1] = num2, num1
    count += 1
    if FLAG:
        return lst, count
    return fun(lst)


if __name__ == '__main__':
    l = []
    while len(l) <= 1000:
        num = round(random.uniform(1, 2), 2)
        if num not in l:
            l.append(num)
    print(l)
    l1 = fun(l)
    print(l1)

