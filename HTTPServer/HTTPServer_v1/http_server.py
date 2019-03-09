# -*- coding: utf-8 -*-
# @Time    : 2019-2-15 11:03
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : http_server.py
# @Software: PyCharm

# http server v1.0
# 接收浏览器请求
# 返回固定的响应内容

from socket import socket, SOL_SOCKET, SO_REUSEADDR

# 处理客户端请求(处理浏览器的请求)
def handle_client(conn_fd):
    print('Connect to the', conn_fd.getpeername())
    request = conn_fd.recv(4096)        # 接收http请求
    for i in request.splitlines():       # 将request按行打印
        print(i)
    try:
        f = open('index.html')
    except IOError:
        response = 'HTTP/1.1 404 NOT FOUND\r\n'
        response += '\r\n'
        response += '<h1>Happy Year...</h1>'
    else:
        response = 'HTTP/1.1 200 OK\r\n'
        response += '\r\n'
        response += f.read()
    finally:
        conn_fd.send(response.encode())

# 创建套接字
def main():
    sock_fd = socket()
    sock_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    sock_fd.bind(('0.0.0.0', 7777))
    sock_fd.listen(5)
    print('Listen to the port 7777 ...')
    while True:
        conn_fd, addr = sock_fd.accept()
        handle_client(conn_fd)            # 负责具体的请求处理
        conn_fd.close()


if __name__ == '__main__':
    main()
