# coding=utf-8
# @Time    : 19-2-25 下午2:12
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : http_server.py
# @Software: PyCharm

'''
HTTP Server v2.0
* 多线程并发
* 基本的request解析
* 能够反馈基本数据
* 使用类封装
'''

from socket import *
from threading import Thread
import sys

# 封装具体的类作为HTTP Server功能模块
class HTTPServer(object):
    def __init__(self, addr, static_dir):
        # 添加对象属性
        self.addr = addr
        self.create_socket()
        self.bind()
        self.static_dir = static_dir
    def create_socket(self):
        self.sock_fd = socket()
        self.sock_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self):
        self.sock_fd.bind(self.addr)
        self.ip = self.addr[0]
        self.port = self.addr[1]

    def serve_forever(self):
        self.sock_fd.listen(5)
        print('Listen the port %d' % self.port)
        while True:
            try:
                conn, addr = self.sock_fd.accept()
            except KeyboardInterrupt:
                self.sock_fd.close()
                sys.exit('服务端退出')
            except Exception as e:
                print('Error:', e)
                continue
            # 创建多线程
            client_thread = Thread(target=self.handle, args=(conn,))
            client_thread.setDaemon(True)
            client_thread.start()

    def handle(self, conn):
        while True:
            # 接收HTTP请求
            try:
                request = conn.recv(4096)
            except KeyboardInterrupt:
                sys.exit('客户端退出...')
            except Exception as e:
                print('Error:', e)
                continue
            # 防止浏览器异常断开
            if not request:
                conn.close()
                return
            # 请求解析
            requestHeaders = request.splitlines()
            # 获取请求内容,bytes没有split()方法
            getRequest = str(requestHeaders[0]).split()[1]
            print(conn.getpeername() ,":", getRequest)
            if getRequest == '/' or '.html' in getRequest[-5:]:
                print('想获取网页')
                self.get_html(conn, getRequest)
            else:
                print('想获取其它内容')
                self.get_data(conn, getRequest)

    def get_html(self, conn, getRequest):
        if getRequest == '/':
            file_name = self.static_dir + '/index.html'
        else:
            file_name = self.static_dir + getRequest
        try:
            f = open(file_name)
        except IOError:
            # 没有找到网页
            responseHeaders = 'HTTP/1.1 404 Not Found\r\n'
            responseHeaders += '\r\n'
            responseBody = 'Sorry,Not found the page'
        else:
            # 返回网页内容
            responseHeaders = 'HTTP/1.1 200 OK\r\n'
            responseHeaders += '\r\n'
            responseBody = f.read()
        finally:
            response = responseHeaders + responseBody
        conn.send(response.encode('utf-8'))

    def get_data(self, conn, getRequest):
        # 返回网页内容
        responseHeaders = 'HTTP/1.1 200 OK\r\n'
        responseHeaders += '\r\n'
        responseBody = '<h1>Waiting for HTTPServer v3.0</h1>'
        response = responseHeaders + responseBody
        conn.send(response.encode('utf-8'))

if __name__ == '__main__':
    # 用户设定ip,host
    ADDR = ('0.0.0.0', 6288)
    # 用户提供存放网页的目录
    static_dir = './static'
    # 创建服务器对象
    httpd = HTTPServer(ADDR, static_dir)
    # 启动服务
    httpd.serve_forever()