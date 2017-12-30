import requests
import re
import time
from lxml import etree
from retrying import retry


class LaGou(object):
    # 拉钩招聘
    def __init__(self, page):
        self.start_url = 'https://www.lagou.com/zhaopin/'
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        self.headers = {"User-Agent": ua}
        self.error = False
        self.error_page = 1
        self.page = page

    @retry(stop_max_attempt_number=5)
    def _parse_url(self, url):
        # 解析网址
        response = requests.get(url, headers=self.headers, timeout=3)
        assert response.status_code == 200

        return response.content.decode()

    def parse_url(self, url):
        page = None
        try:
            print('now parsing{}'.format(url))
            page = re.findall('\d+', url)[0]
            html = self._parse_url(url)
            title = re.findall("职位列表", html)
            if len(title) == 0:
                print('错误信息', title)
                print('网页反爬,暂停...')
                self.error = True
                self.error_page = int(page)
                return None, page

        except Exception as e:
            print(e, '无法解析的地址')
            html = None
        return html, page

    def parse_list_info(self, html, page):
        # 解析列表页数据
        if html is None:
            return
        html = etree.HTML(html)
        li_list = html.xpath("//li[@class='con_list_item default_list']")
        for li in li_list:
            item = dict()
            title = li.xpath(".//a[@class='position_link']/h3/text()")
            item["title"] = title[0] if len(title) > 0 else None
            print(item["title"])
        print('*'*50, '当前页数为:', page)

    def url_change(self, url):
        # 主要逻辑函数
        html, page = self.parse_url(url)
        self.parse_list_info(html, page)

    def run(self):
        # url调度器
        for i in range(self.page, 31):
            if self.error:
                return
            time.sleep(1)
            next_url = self.start_url + str(i)
            self.url_change(next_url)


if __name__ == '__main__':
    lagou = LaGou(1)
    lagou.run()
    while lagou.error:
        time.sleep(20)
        lagou = LaGou(lagou.error_page)
        lagou.run()
