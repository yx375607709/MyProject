# -*- coding: utf-8 -*-
# @Time    : 19-2-21 下午3:48
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : thread_excise.py
# @Software: PyCharm

from threading import Thread
from time import sleep, ctime

class MyThread(Thread):
    def __init__(self, target=None, args=(),
                 kwargs={}, name='Thread-1'):
        super(MyThread, self).__init__()
        self.func = target
        self.sec = args
        self.song = kwargs
        self.name = name

    def run(self):
        self.func(*self.sec, **self.song)

def player(sec, song):
    for i in range(2):
        print('Playing %s:%s' % (song, ctime()))
        sleep(sec)

t = MyThread(target=player, args=(3,), kwargs={'song':'凉凉'}, name='happy')

t.start()
t.join()