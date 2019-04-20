import timeit
import gevent
from gevent.pool import Pool
from config import HTTP_TEST_URL
from requests.exceptions import ProxyError, ConnectTimeout, \
    SSLError, ReadTimeout, ConnectionError, ChunkedEncodingError
import requests


x = Pool(80)
statistics = [0, 0]


def async1():
    for i in range(30):
        statistics[0] += 1
        print(statistics[0])
        x.imap_unordered(task1)


def task1():
    try:
        r = requests.get(HTTP_TEST_URL, timeout=5)
    except:
        pass


def sync():
    for i in range(30):
        statistics[1] += 1
        print('同步爬虫任务......',statistics[1])
        task1()


print(timeit.timeit(stmt=async1, setup='''
from __main__ import task1, async1, sync
''', number=100))
print('同步开始了', statistics[0])
print(timeit.timeit(stmt=sync, setup='''from __main__ import task1, async1, sync''', number=100))
print(statistics)