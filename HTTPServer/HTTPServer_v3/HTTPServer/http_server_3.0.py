# coding=utf-8
# @Time    : 19-2-25 下午2:12
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : http_server.py
# @Software: PyCharm

'''
HTTP Server v3.0
'''

from threading import Thread
import sys
# 导入配置信息
from HTTPServer_v3.Web_Frame.web_frame import *
from HTTPServer_v3.HTTPServer.config import *

# 向frame发送请求
def connect_frame(**kwargs):
    s = socket()
    try:
        s.connect(frame_address)
    except Exception as e:
        print(e)
        return
    s.send(json.dumps(kwargs).encode())
    data = s.recv(4096).decode()
    return data





# 封装具体的类作为HTTP Server功能模块
class HTTPServer(object):
    def __init__(self):
        # self.addr = addr
        self.create_socket()
        self.bind(ADDR)
        self.server_forever()

    # 创建套接字
    def create_socket(self):
        self.sock_fd = socket()
        # 设置端口重用
        self.sock_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self,address):
        self.ip = address[0]
        self.port = address[1]
        self.sock_fd.bind(address)

    # 启动服务
    def server_forever(self):
        while True:
            # 开始监听客户端
            self.sock_fd.listen(10)
            try:
                conn, add = self.sock_fd.accept()
            except KeyboardInterrupt:
                self.sock_fd.close()
                sys.exit('服务端退出...')
            except Exception as e:
                print('e')
                continue
            # 创建子线程
            client = Thread(target=self.handle, args=(conn,))
            client.setDaemon(True)
            client.start()

    def handle(self, conn):
        request = conn.recv(4096)
        # 处理客户端断开
        if not request or request[0] == 'Q':
            conn.close()
            return

        # 处理客户端请求
        request_lines = request.splitlines()
        request_line = request_lines[0].decode('utf-8')
        tmp = request_line.split(' ')
        method = tmp[0]
        path_info = tmp[1]
        data = connect_frame(method=method, path_info=path_info)
        self.response(data, conn)

    # 给客户端返回响应{status:200, data:xxxxxx}
    def response(self, data, conn):
        # 根据情况组织响应
        if data == '200':
            response_headers = 'HTTP/1.1 200 OK\r\n'
        elif data == '404':
            response_headers = 'HTTP/1.1 404 Not Found\r\n'
        else:
            response_headers = 'HTTP/1.1 888 Unknown Error\r\n'
        response_headers += '\r\n'
        response_body = data
        response = (response_headers + response_body).encode('utf-8')
        conn.send(response)
        conn.close()




if __name__ == '__main__':
    # app = Application()
    # app.start()
    httpd = HTTPServer()
    httpd.server_forever() # 启动服务程序