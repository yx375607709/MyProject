# -*- coding: utf-8 -*-
# @Time    : 19-2-22 下午3:15
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : main.py
# @Software: PyCharm

from socket import *
import os
import signal
import sys
import struct

# 创建服务器类
class FtpServer(object):
    def __init__(self, addr):
        self.start_server(addr)

    def start_server(self, addr):
        '''服务器运行'''
        self.sock_fd = socket()
        # 设置套接字重用
        self.sock_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # 设置信号避免僵尸进程
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        self.sock_fd.bind(addr)
        self.sock_fd.listen(5)
        while True:
            try:
                self.conn, addr = self.sock_fd.accept()
            except KeyboardInterrupt:
                sys.exit('服务端退出...')
            except Exception as e:
                print(e)
                continue
            # 创建子进程处理客户端请求
            pid = os.fork()
            if pid == 0:
                # 子进程执行事件
                self.sock_fd.close()
                print('客户端连接:', self.conn.getpeername())
                # 子进程处理客户端请求接口
                self.handle_client()
                sys.exit('客户端退出...')
            else:
                # 父进程关闭客户端连接,等待其它客户端连接
                self.conn.close()

    def handle_client(self):
        # 循环处理客户端请求
        new_file = 'newfile'
        while True:
            data = self.recv_message_server()
            if data[:2] == 'C ':
                # 客户端发送文件字典信息
                self.show_file_names()
            elif data[:2] == 'S ':
                #　向客户端发送文件
                self.download_file(data[2:])
            elif data[:2] == 'L ':
                # 接收客户端文件
                self.add_file(new_file, data[2:])
            elif data[:2] == 'F ':
                # 判断文件是否存在
                file = self.file_exists(data[2:])
                if file:
                    new_file = file
            elif data[:2] == 'Q ':
                # 判断客户端退出
                sys.exit('客户端退出...')

    def file_exists(self, filename):
        # 判断文件是否存在,如果存在发送'P ',不存在发送'K '
        if os.path.exists('myfile/' + filename):
            data = 'P '
            self.send_message_server(data)
        else:
            data = 'K ' + filename
            self.send_message_server(data)
            return filename

    def add_file(self, filename, data):
        #　服务端写入文件
        with open('myfile' + '/' + filename.split('/')[1], 'a') as f:
            f.write(data)
            f.flush()
        # 像客户端发送接收信号
        data = 'E ' + 'myfile' + '/' + filename.split('/')[1]
        self.send_message_server(data)

    def download_file(self, filename):
        #　发送文件给客户端，发送完成发送＇G＇
        with open('myfile/' + filename, 'r') as f:
            file_size = os.path.getsize('myfile/' + filename)
            while True:
                if file_size > 1024:
                    data = 'F '+ f.read(1024)
                    self.send_message_server(data)
                    file_size -= 1024
                else:
                    data = 'F '+ f.read(file_size)
                    self.send_message_server(data)
                    break
            data = 'G '
            self.send_message_server(data)

    def show_file_names(self):
        # 发送文件名称字典
        file_names = 'N ' + str(dict(enumerate(filter(lambda f: not os.path.isfile(f),
                                                      os.listdir('myfile')), start=1)))
        self.send_message_server(file_names)

    def recv_message_server(self):
        # 接收客户端请求
        data = self.conn.recv(4)
        if not data:
            sys.exit('客户端退出...')
        data_size = struct.unpack('i', data)[0]
        return self.conn.recv(data_size).decode('utf-8')

    def send_message_server(self, data):
        # 发送客户端请求结果
        data_size = struct.pack('i', len(data.encode('utf-8')))
        send_data = data_size + data.encode('utf-8')
        self.conn.send(send_data)

if __name__ == '__main__':
    server = FtpServer(('0.0.0.0', 6666))
