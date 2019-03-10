# !/usr/bin/python3
# coding=utf-8
# @Time    : 19-3-10 下午2:07
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : webf_rame.py
# @Software: PyCharm

from socket import *
from select import select
import json

# 导入配置信息
from HTTPServer_v3.Web_Frame.settings import *

'''
模拟网站后端应用处理程序
httpserver3.0
'''

# 创建应用类处理具体请求
class Application(object):
    def __init__(self):
        self.ip = frame_address[0]
        self.port = frame_address[1]
        self.sock_app = socket()
        self.sock_app.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock_app.bind(frame_address)

    def start(self):
        self.sock_app.listen(5)
        print('Listen the port %s' % self.port)
        rlist = [self.sock_app]
        wlist = []
        xlist = []
        while True:
            rs, ws, xs = select(rlist, wlist, xlist)
            for r in rs:
                if r is self.sock_app:
                    conn, addr = r.accept()
                    rlist.append(conn)
                else:
                    # 接收httpserver请求
                    request = r.recv(1024).decode('utf-8')
                    # 如过客户端退出,移除select对象
                    if not request:
                        rlist.remove(r)
                        continue
                    self.handle(r, request)


    def handle(self, conn, request):
        request = json.loads(request)
        method = request['method']
        path_info = request['path_info']

        if method == 'GET':
            if path_info == '/' or path_info[-5] == '.html':
                data = self.get_html(path_info)
            else:
                data = self.get_data(path_info)
        elif method == 'POST':
            pass

        # 得到网页内容则发送,没有得到就发送404
        if data:
            print('1234')
            conn.send(data.encode('utf-8'))
        else:
            conn.send(b'404')

    def get_html(self, path_info):
        if path_info == '/':
            filename = STATIC_DIR + 'bilibili.html'
        else:
            filename = STATIC_DIR + path_info
        try:
            fd = open(filename, 'r')
        except IOError:
            # 没有找到网页
            print('没有找到网页')
            return
        else:
            # 返回网页内容
            return fd.read()

    def get_data(self,path_info):
        if path_info in urls:
            return urls[path_info]
        else:
            return '404'




if __name__ == '__main__':
    app = Application()
    app.start()
    # with open('static/bilibili.html') as f:
    #     print(f.read())