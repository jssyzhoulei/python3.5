import socket
import re
import gevent
import sys
from gevent import monkey
monkey.patch_all()


class HTTPserver(object):
    """miniweb服务器接收响应数据
    配合框架端组建静态、动态响应报文
    """
    def __init__(self,app,port=8080):
        # 初始化服务器创建套接字
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 复用连接、绑定端口
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        self.server_socket.bind(('',port))
        self.server_socket.listen(128)
        # 调用框架
        self.app = app

    def run_forever(self):
        # 运行服务器循环接收HTTP请求
        while True:
            # 接收浏览器请求
            client_socket,remote_adress = self.server_socket.accept()
            # 协程实现多任务
            gevent.spawn(self.deal_with_request, client_socket, remote_adress)

    def deal_with_request(self, client_socket, remote_adress):
        # 接收请求、处理响应数据
        print('开始为%s服务' % str(remote_adress))
        request_data = client_socket.recv(1024).decode()
        request_lines = request_data.splitlines()
        # 分析请求头，匹配出地址
        # GET /path http/1.1
        ret = re.search(r'\s*[^ ]+\s+(/[^ ]*)',request_lines[0])
        # ret = re.search(r"^(\w+)\s+([/.\w\-]+) ", request_lines[0])
        if not ret:#如果没有匹配到数据
            print('没有匹配到数据')
            client_socket.close()
            return

        # 处理匹配到的网址
        file_name = ret.group(1)
        if file_name == '/':
            file_name = '/index.html'

        # 创建字典存放文件地址、传递到框架中处理
        env = dict()
        env['FILE_NAME'] = file_name
        response_body = self.app(env,self.start_response)
        # 发送报文
        client_socket.send(self.response_headers.encode() + response_body)
        client_socket.close()

    def start_response(self,status,response_list):
        # 设置响应头相关信息，将响应头编码好byte格式,注意\r\n位置
        self.response_headers = ''
        # 响应报文头如 'HTTP/1.1 200 OK'
        response = 'HTTP/1.1 %s\r\n' %status
        for key,value in response_list:
            response += '%s: %s\r\n'%(key,value)
            # 请求名和请求值之间用：（冒号加空格隔开）
        response += '\r\n'
        # 组建响应头对象属性
        self.response_headers = response


def main():
    if len(sys.argv) < 2:
        print('输入格式错误')
        print(sys.argv)
        return
    else:
        module_name = sys.argv[1]

    # 终端命令形如 webserver:app
    module_names_list = module_name.split(':')
    if len(module_names_list) != 2:
        print(module_names_list)
        print('框架应用模块输入有误')
        return
    try:
        print(module_names_list)
        mod_obj = __import__(module_names_list[0])
        app = getattr(mod_obj,module_names_list[1])

    except:
        print('无法匹配到相应框架/模块')
        return
    # 创建服务器对象
    httpd = HTTPserver(app)
    httpd.run_forever()

if __name__ == '__main__':
    main()