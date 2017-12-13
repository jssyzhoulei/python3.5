# 应用框架端代码实现

import re
import functools
import pymysql
import time

route_list = []
LOCK_ROOT = '.'

# 装饰器工厂实现路由
def route(path='/index.html'):
    def wrapper(func):
        # 把预设的路径、函数添加到列表中
        route_list.append((path,func))
        @functools.wraps(func)
        def inner(*args):

            return func()
        return inner
    return wrapper

@route('/gettime.html')
def gettime():
    print(gettime.__name__)
    return time.ctime()

@route('/index.html')
def index():
    return """hello python
    尝试一下看看能否显示中文
    当前时间是：北京时间%s
    赵宝宝是笨蛋
    您所访问的服务器地址在苏州新区科技城新和信息科技"""%time.ctime()

@route('/stockinfo/(\d{6})\.html')
def select_stock_info(url,file_name):
    ret = re.match(url,file_name)
    stock_code = ret.group(1)
    # 创建pymysql连接
    psw = 'mysql'
    con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password=psw, db='stock_db', charset='utf8')
    cur = con.cursor()
    sql = 'select * from info where code = %s'%stock_code
    try:
        cur.execute(sql)
        # 取得返回的元祖、切片出有用数据
        ret = cur.fetchall()[0][1:]
    except:
        return None
    else:
        html = """<!DOCTYPE html><html lang="zh"><head>
                <meta charset="UTF-8"><title>信息</title></head><body><tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td><td>
                <a type="button" class="btn btn-default btn-xs" href="/index.html">
                    <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                </td><td><input type="button" value="删除" id="toDel" name="toDel" >
                </td></tr>
                </body>
                </html>"""
        print('正在匹配数据库中内容.....消息来自小周的程序，，，')
        ret = html%ret

        # 提交修改
        con.commit()
        # 关闭资源
        cur.close()
        con.close()

        return ret


# 列表存放路由：格式为 (文件名（url）,对应方法)
class Application(object):
    def __init__(self,route_list):
        self.route_list = route_list

    def __call__(self, env, start_response):
        """将类的对象设置为可调用对象
        __call__方法内的代码为调用对象时执行"""
        file_name = env['FILE_NAME']
        response_list = [('HTTPsever','Pythonversion 8.0')]
        for url,func in self.route_list:
            if url == file_name:
                response_body = func()
                # 组建响应头
                status = '200 OK'
                start_response(status,response_list)
                # 返回响应体，注意要编码成byte类型
                return response_body.encode('gbk')

            # ret = re.martch(r'/stock/\d{6}\.html',file_name)
            ret = re.match(url,file_name)
            # 如果请求文件和列表中文件匹配
            if ret:
                # 调用被装饰器工厂返回的装饰器函数
                rst = func(url,file_name)
                if rst:
                    status = '200 OK'
                    start_response(status, response_list)
                    return rst.encode()
                else:
                    status = '404 Not Found'
                    start_response(status, response_list)
                    # 装饰器函数错误、返回空值

                    return 'error_neiceng'.encode()

        else:#无法匹配到到列表内容、则请求的是普通文件
            try:
                f = open(LOCK_ROOT+file_name,'rb')
            except: #无效的请求地址
                status = '404 Not Found'
                start_response(status, response_list)
                return '请求资源有误'.encode('gbk')
            else:
                content = f.read()
                f.close()
                status = '200 OK'
                start_response(status, response_list)
                return content

app = Application(route_list)
# 服务器端可以通过app（参数）的方式调用对象