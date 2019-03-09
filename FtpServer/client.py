# -*- coding: utf-8 -*-
# @Time    : 19-2-22 下午11:08
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : client.py
# @Software: PyCharm

from socket import *
import os
import signal
import sys
import struct

# 创建客户端类
class FtpClient(object):
    def __init__(self, addr):
        self.start_client(addr)

    def start_client(self, addr):
        '''开始执行客户端程序'''
        self.sock_fd = socket()
        self.sock_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        #　设置signal信号,防止僵尸进程产生
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        self.sock_fd.connect(addr)
        print('连接服务器成功...')
        while True:
            try:
                # 循环客户端处理事件方法
                self.handle_server()
            except KeyboardInterrupt:
                self.send_message_client('QUIT')
                sys.exit('客户端退出...')
            except Exception as e:
                self.send_message_client('QUIT')
                print(e)
                sys.exit('未知错误,请联系管理员...')

    def handle_server(self):
        while True:
            # 运行开始选择程序,判断下载或上传
            choose = self.start_choose()
            file_name = 'new_file'
            if choose == 'load':
                self.loadfile()
            elif choose == 'down':
                data = 'C '
                self.send_message_client(data)
            while True:
                data = self.recv_message_client()
                # 如果服务器回复'N ',则表示传送过来文件字典
                if data[:2] == 'N ':
                    # 调用self.print_choose()方法,进行文件选择,并返回文件名称
                    file_name = self.print_choose(data[2:])
                elif data[:2] == 'F ':
                    # 如果服务器返回'F ',说明传送过来文件
                    self.download_file(data[2:], file_name)
                elif data[:2] == 'E ':
                    print('上传成功,文件路径:', data[2:])
                    break
                elif data[:2] == 'G ':
                    print('下载成功,文件路径:', file_name)
                    break
                elif data[:2] == 'P ':
                    print('该文件已经存在...\n')
                    self.loadfile()
                elif data[:2] == 'K ':
                    # 上传文件给服务器
                    self.send_file_to_server(data[2:])
    def loadfile(self):
        while True:
            file_parent = input('请输入上传文件夹名称:\n')
            if not file_parent:
                print('文件夹名不能为空,请重新输入...')
                continue
            if len(file_parent) > 1:
                if file_parent[1] == ' ':
                    print('输入内容第二位不能为空,请重新输入..')
                    continue
            if not os.path.exists(file_parent):
                print('该文件夹不存在,请重新选择...')
            elif not os.listdir(file_parent):
                print('文件夹下面没有文件,请重新选择...')
            else:
                break
        while True:
            file_dict = dict(enumerate(os.listdir(file_parent), start=1))
            for k, v in file_dict.items():
                print('编号: %s    ,文件名: %s' % (k, v))
            try:
                number = int(input('请选择文件编号:\n'))
            except ValueError:
                print('输入错误请重新选择...')
                continue
            else:
                if number in file_dict:
                    file = file_dict[number]
                    break
                else:
                    print('选择编号超出范围...')
        self.send_message_client('F ' + file_parent + '/' + file)

    def send_file_to_server(self, file):
        # 设置每次发送接收最大1024字节
        with open(file, 'r', encoding='utf-8') as f:
            file_size = os.path.getsize(file)
            while True:
                if file_size > 1024:
                    data = 'L ' + f.read(1024)
                    self.send_message_client(data)
                    file_size -= 1024
                else:
                    data = 'L ' + f.read(file_size)
                    self.send_message_client(data)
                    break

    def download_file(self, data, file_name):
        with open(file_name,'a', encoding='utf-8') as f:
            f.write(data)
            f.flush()

    def recv_message_client(self):
        # 每次先接收4字节文件,表示的是文件大小,再接收文件,避免产生粘包
        data_size = struct.unpack('i', self.sock_fd.recv(4))[0]
        return self.sock_fd.recv(data_size).decode('utf-8')

    def send_message_client(self, data):
        # 先生成4字节文件大小,再进行文件发送,避免粘包
        data_size = struct.pack('i', len(data.encode('utf-8')))
        send_data = data_size + data.encode('utf-8')
        self.sock_fd.send(send_data)

    def start_choose(self):
        while True:
            try:
                number = int(input('下载请输入: 1\n上传请输入: 2\n退出请输入: 3\n'))
            except ValueError:
                print('输入错误,请仔细检查后再次输入...')
                continue
            else:
                if number in (1, 2, 3):
                    if number == 3:
                        self.send_message_client('Q ')
                        sys.exit('您选择退出...')
                    elif number == 2:
                        return 'load'
                    else:
                        return 'down'
                else:
                    print('输入错误,请认真输入...')

    def print_choose(self, data):
        for k, v in eval(data).items():
            print('编号: %s   文件: %s' % (k, v))
        while True:
            try:
                number = int(input('请选择下载编号:\n'))
            except ValueError:
                print('选择错误,请仔细选择...')
            except Exception as e:
                print(e)
            else:
                if number in eval(data):
                    self.send_message_client(('S ' + eval(data)[number]))
                    while True:
                        file = input('请输入保存文件夹名称:\n')
                        if not file:
                            print('文件名不能为空,请重新输入...')
                            continue
                        if len(file) > 1:
                            if file[1] == ' ':
                                print('输入内容第二位不能为空,请重新输入..')
                                continue
                        if os.path.exists(file):
                            choose = input('该文件夹已经存在,坚持使用这个文件夹吗(yes or no)?\n')
                            if choose == 'yes':
                                break
                        else:
                            os.mkdir(file)
                            break
                    while True:
                        file_name = input('请输入新文件名称:\n')
                        if not file_name:
                            print('文件名不能为空,请重新输入...')
                            continue
                        if len(file_name) > 1:
                            if file_name[1] == ' ':
                                print('输入内容第二位不能为空,请重新输入..')
                                continue
                        if os.path.exists(file + '/' + file_name):
                            choose = input('该文件已经存在,替换原文件吗(yes or no)?\n')
                            if choose == 'yes':
                                os.remove(file + '/' + file_name)
                                break
                        else:
                            break
                    return file + '/' + file_name
                else:
                    print('编号选择错误,请重新选择.v..')


if __name__ == '__main__':
    client = FtpClient(('103.46.128.41', 57550));' '