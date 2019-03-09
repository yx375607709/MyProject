# -*- coding: utf-8 -*-
# @Time    : 19-2-22 下午2:28
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : ftp_server.py
# @Software: PyCharm


from socket import *
import os
import signal
import sys
import struct

class FtpServer(object):
    def __init__(self, addr):
        self.start_server(addr)

    def start_server(self, addr):
        self.sock_fd = socket()
        self.sock_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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
            pid = os.fork()
            if pid == 0:
                self.sock_fd.close()
                print('客户端连接:', self.conn.getpeername())
                self.handle_client()
                sys.exit('客户端退出...')
            else:
                self.conn.close()

    def handle_client(self):
        new_file = 'newfile'
        while True:
            data = self.recv_message_server()
            if data[:2] == 'C ':
                self.show_file_names()
            elif data[:2] == 'S ':
                self.download_file(data[2:])
            elif data[:2] == 'L ':
                self.add_file(new_file, data[2:])
            elif data[:2] == 'F ':
                file = self.file_exists(data[2:])
                if file:
                    new_file = file
    def file_exists(self, filename):
        if os.path.exists('myfile/' + filename):
            data = 'P '
            self.send_message_server(data)
        else:
            data = 'K ' + filename
            self.send_message_server(data)
            return filename

    def add_file(self, filename, data):
        with open('myfile' + '/' + filename, 'a') as f:
            f.write(data)
            f.flush()
        data = 'E '
        self.send_message_server(data)

    def download_file(self, filename):
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
            data = 'E '
            self.send_message_server(data)

    def show_file_names(self):
        file_names = 'N ' + str(dict(enumerate(filter(lambda f: not os.path.isfile(f),
                                                      os.listdir('myfile')), start=1)))
        self.send_message_server(file_names)

    def recv_message_server(self):
        data = self.conn.recv(4)
        if not data:
            sys.exit('客户端退出...')
        data_size = struct.unpack('i', data)[0]
        return self.conn.recv(data_size).decode('utf-8')

    def send_message_server(self, data):
        data_size = struct.pack('i', len(data.encode('utf-8')))
        send_data = data_size + data.encode('utf-8')
        self.conn.send(send_data)




# class Ftpclient(object):
#     def __init__(self, addr):
#         self.start_client(addr)
#
#     def start_client(self, addr):
#         self.sock_fd = socket()
#         self.sock_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#         signal.signal(signal.SIGCHLD, signal.SIG_IGN)
#         self.sock_fd.connect(addr)
#         print('连接服务器成功...')
#         while True:
#             try:
#                 self.handle_server()
#             except KeyboardInterrupt:
#                 self.send_message_client('QUIT')
#                 sys.exit('客户端退出...')
#             except Exception as e:
#                 self.send_message_client('QUIT')
#                 print(e)
#     def handle_server(self):
#         self.start_choose()
#         while True:
#             data = self.recv_message_client()
#             if data[:2] == 'N ':
#                 self.print_choose(data[2:])
#
#     def recv_message_client(self):
#         data_size = struct.unpack('i', self.sock_fd.recv(4))[0]
#         return self.sock_fd.recv(data_size).decode('utf-8')
#
#
#     def send_message_client(self, data):
#         data_size = struct.pack('i', len(data.encode('utf-8')))
#         send_data = data_size + data.encode('utf-8')
#         self.sock_fd.send(send_data)
#
#     def start_choose(self):
#         while True:
#             try:
#                 number = int(input('下载请输入:1,上传请输入:2,退出请输入:3\n'))
#             except ValueError:
#                 print('输入错误,请认真输入...')
#                 continue
#             else:
#                 if number in (1, 2, 3):
#                     if number == 3:
#                         sys.exit('您选择退出...')
#                     else:
#                         break
#                 else:
#                     print('输入错误,请认真输入...')
#         data = 'C ' + str(number)
#         self.send_message_client(data)
#
#     def print_choose(self, data):
#         for k, v in eval(data).items():
#             print('编号: %s   文件: %s' % (k, v))
#         while True:
#             try:
#                 number = int(input('请选择下载编号:\n'))
#             except ValueError:
#                 print('选择错误,请仔细选择...')
#             except Exception as e:
#                 print(e)
#             else:
#                 if number in data:
#                     self.sock_fd.send(('S ' + data[number]).encode('utf-8'))
#                     break

if __name__ == '__main__':
    ftp_client = Ftpclient(('127.0.0.1', 6666))


