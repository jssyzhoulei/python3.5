# coding=utf-8
from lxml import etree
from utils import parse_url
import time
import json

"http://www.ip181.com/"
"https://ip.ihuan.me/?page=1&address=5Lit5Zu9"
"http://www.66ip.cn/areaindex_1/1.html"
"http://www.kuaidaili.com/free/inha/"
"http://www.xicidaili.com/"


class ProxyMetaclass(type):
    """
    元类，在ProxyGetter类中加入
    __CrawlFunc__和__CrawlFuncCount__两个参数
    分别表示爬虫函数和爬虫函数的数量
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k in attrs.keys():
            if k.startswith('proxy_'):
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class ProxyGetter(object, metaclass=ProxyMetaclass):

    def get_raw_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    # def proxy_ip181(self):
    #     url = 'http://www.ip181.com/'
    #     resp = parse_url(url)
    #     html = etree.HTML(resp)
    #     ips = html.xpath('//div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr/td[1]/text()')[1:]
    #     ports = html.xpath('//div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr/td[2]/text()')[1:]
    #     for ip, port in zip(ips, ports):
    #         proxy = ip + ':' + port
    #         yield proxy

    # def proxy_ip66(self):
    #     for page in range(1, 9):
    #         url = 'http://www.66ip.cn/areaindex_{}/1.html'.format(page)
    #         resp = parse_url(url)
    #         html = etree.HTML(resp)
    #         ips = html.xpath('//*[@id="footer"]/div/table/tr/td[1]/text()')[1:]
    #         ports = html.xpath('//*[@id="footer"]/div/table/tr/td[2]/text()')[1:]
    #         for ip, port in zip(ips, ports):
    #             proxy = ip + ':' + port
    #             yield proxy

    # def proxy_xici(self):
    #     url = 'http://www.xicidaili.com/'
    #     try:
    #         resp = parse_url(url)
    #     except:
    #         return []
    #     html = etree.HTML(resp)
    #     ips = html.xpath('//*[@id="ip_list"]/tr/td[2]/text()')
    #     https = html.xpath('//*[@id="ip_list"]/tr/td[6]/text()')
    #     ports = html.xpath('//*[@id="ip_list"]/tr/td[3]/text()')
    #     for http, ip, port in zip(https, ips, ports):
    #         proxy = ip + ':' + port
    #         yield proxy

    # def proxy_kuai(self):
    #     for page in range(1, 4):
    #         url = 'http://www.kuaidaili.com/free/inha/{}/'.format(page)
    #         resp = parse_url(url)
    #         try:
    #             html = etree.HTML(resp)
    #             ips = html.xpath('//*[@id="list"]/table/tbody/tr/td[1]/text()')
    #             ports = html.xpath('//*[@id="list"]/table/tbody/tr/td[2]/text()')
    #             for ip, port in zip(ips, ports):
    #                 proxy = ip + ':' + port
    #                 yield proxy
    #         except:
    #             pass

    # def proxy_xun(self):
    #     url = 'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page={}&rows=10'
    #     for page in range(1, 4):
    #         try:
    #             resp = parse_url(url.format(page))
    #             html = json.loads(resp)
    #             ips = [i['ip'] for i in html['RESULT']['rows']]
    #             ports = [i['port'] for i in html['RESULT']['rows']]
    #             for ip, port in zip(ips, ports):
    #                 proxy = ip + ':' + port
    #                 yield proxy
    #         except:
    #             return []

    # def proxy_ihuan(self):
    #     for page in range(1, 4):
    #         url = 'https://ip.ihuan.me/?page={0}&address=5Lit5Zu9'.format(page)
    #         resp = parse_ihun(url, page)
    #         html = etree.HTML(resp)
    #         ips = html.xpath('/html/body/div[2]/div[2]/table/tbody/tr/td[1]/a/text()')
    #         ports = html.xpath('/html/body/div[2]/div[2]/table/tbody/tr/td[2]/text()')
    #         for ip, port in zip(ips, ports):
    #             proxy = ip + ':' + port
    #             yield proxy
    def proxy_zhimas(self):
        url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=' \
              '&city=0&yys=0&port=1&pack=19967&ts=0&ys=0&cs=1&lb=1&sb=0&pb=45&mr=1&regions='
        resp = parse_url(url)
        print(resp)
        html = json.loads(resp)
        code = html.get('code')
        success = html.get('success')
        if code != 0 or success == 'false':
            return
        datas = html.get('data')
        for data in datas:
            yield data.get('ip') + ':' + str(data.get('port'))

    def proxy_zhima(self):
        url = 'http://webapi.http.zhimacangku.com/getip?num=2&type=2&pro=&city=0&yys=0' \
              '&port=1&pack=19337&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
        resp = parse_url(url)

        html = json.loads(resp)
        code = html.get('code')
        success = html.get('success')
        if code != 0 or success == 'false':
            print(html)
            return
        datas = html.get('data')
        for data in datas:
            yield data.get('ip') + ':' + str(data.get('port'))


if __name__ == '__main__':
    pg = ProxyGetter()
    s = pg.proxy_zhimas()
    for i in s:
        print(i)
