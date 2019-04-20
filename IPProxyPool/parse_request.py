from get_proxy import ProxyGetter
from gevent import pool


pg = ProxyGetter()
# s = pg.proxy_xici()
# print(s)
# for i in s:
#     print(i)

# proxy_xici    ok
# proxy_kuai    ok
# proxy_ip66   no
# proxy_ip181  no

import time


def my_f():
    def my_2():
        time.sleep(1)
        xin.append('en')
    luo.append('ai')
    while True:
        xin = []
        if True:
            my_2()
        time.sleep(3)

        return [xin, luo]

luo = []
s = my_f()
print(s)



# gevent 示例


from bs4 import BeautifulSoup
import requests
import gevent
from gevent import monkey, pool
monkey.patch_all()

jobs = []
links = []
p = pool.Pool(10)

urls = [
    'http://www.google.com',
    # ... another 100 urls
]

def get_links(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text)
        links + soup.find_all('a')

for url in urls:
    jobs.append(p.spawn(get_links, url))
gevent.joinall(jobs)
