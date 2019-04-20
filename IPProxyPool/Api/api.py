from flask import Flask, g, request
from tester import ProxyTester
from db import MongodbClient

app = Flask(__name__)


def get_conn():
    """
    链接Mongodb
    """
    if not hasattr(g, 'mongodb_conn'):
        g.mongodb_conn = MongodbClient()
    return g.mongodb_conn


@app.route('/')
def index():
    """
    index html
    """
    return '<h1>IP Proxy Pool</h1>' + '\n' \
        + '<h3>/get: Get a proxy from proxy pool, option arguments https null or not null;</h3>' + '\n' \
        + '<h3>/count: Get number of proxies</h3>'


@app.route('/get')
def get_proxy():
    """
    拿到一个代理
    """
    https = request.args.get('https')
    conn = get_conn()
    if https:
        return conn.pop(True)
    return conn.pop()


@app.route('/firget')
def first_proxy():
    """
    拿到一个代理
    """
    https = request.args.get('https')
    conn = get_conn()
    if https:
        return conn.pop2(True)
    return conn.pop2()


@app.route('/test')
def test_proxy():
    proxy = request.args.get('proxy')
    ts = ProxyTester()
    ts.set_raw_proxies([proxy])
    ts.test()
    return 'start testing'


@app.route('/count')
def count():
    """
    代理总数
    """
    conn = get_conn()
    http, https = conn.get_count
    return 'http:{}, https:{}'.format(http, https)

