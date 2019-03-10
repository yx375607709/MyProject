# !/usr/bin/python3
# coding=utf-8
# @Time    : 19-3-10 上午9:58
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : config.py
# @Software: PyCharm

'''
HTTPServer配置文件,用于填写基本的必要信息
'''

#　配置服务器地址
HOST = '0.0.0.0'
PORT = 7777
ADDR = (HOST, PORT)

# debug 设置True表示调试
DEBUG = True

# 配合的web Frame地址
frame_ip = '127.0.0.1'
frame_port = 8080
frame_address = (frame_ip, frame_port)