# !/usr/bin/python3
# coding=utf-8
# @Time    : 19-3-10 下午2:15
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : settings.py
# @Software: PyCharm

from HTTPServer_v3.Web_Frame.views import *

'''
Frame程序的配置文件
'''

frame_ip = '0.0.0.0'
frame_port = 8080
frame_address = (frame_ip, frame_port)

#静态网页位置
STATIC_DIR = 'static/'


urls = {
    '/time': show_time,
    '/hello': say_hello
}