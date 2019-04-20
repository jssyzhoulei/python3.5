import requests
import time
import random
from config import HTTPS_TEST_URL, HTTP_TEST_URL
from requests.exceptions import ProxyError, ConnectTimeout, \
    SSLError, ReadTimeout, ConnectionError, ChunkedEncodingError


def add_time(lis):
    total = 0
    count = len(lis)
    for i in lis:
        total += i
    return total/count


def test_proxy_time():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    }
    url = 'http://192.168.1.34:5000/get'

    rst = '36.6.140.14:53852'
    rst = HTTPS_TEST_URL
    # print(rst.text)
    proxy = {'http': 'http://' + rst}
    # print(proxy)
    url = 'https://mp.weixin.qq.com/mp/getappmsgext'
    count = 0
    while True:
        timer = time.time()
        used_time = []
        try:
            r = requests.get(url, headers=headers, proxies=proxy, timeout=5)
        except:
            print('连接超时:当前代理持续时间为{}'.format(count * 20))
            break
        if r.status_code == 200:
            use_t = time.time() - timer
            used_time.append(use_t)
            print("请求耗时为", use_t)
            print('当前代理持续时间为{}'.format(count*20))
        else:
            print('当前断开：当前代理持续时间为{}'.format(count*20))
            break
        if count == 6:
            used_tim = add_time(used_time)
            if used_tim < 1:
                print('nice代理', proxy, used_tim)
            else:
                print('6次均时表现一般', proxy, used_tim)
        count += 1
        time.sleep(20)

test_proxy_time()

# index = True
# print(not index)
