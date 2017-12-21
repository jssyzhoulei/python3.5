# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    # 苏宁图书首页
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):

        # 获取大分类列表
        li_list = response.xpath("//ul[@class='ulwrap']/li")
        for li in li_list:
            item = {}
            # 大分类键值
            item["b_cate"]= li.xpath("./div[1]/a/text()").extract_first()
            # 小分类列表
            a_list = li.xpath("./div[2]/a")
            for a in a_list:
                # 获取小分类以及url地址
                item["s_cate"] = a.xpath("./text()").extract_first()
                item["href"] = a.xpath("./@href").extract_first()
                if item["href"] is not None:
                    item["href"] = "http://snbook.suning.com"+item["href"]

                # 请求图素列表详情页
                yield scrapy.Request(
                    item["href"],
                    callback=self.book_list_parse,
                    meta= {"item":deepcopy(item)}
                )

    def book_list_parse(self,response):
        # 提取详情页的数据
        item = response.meta["item"]
        # 图书详情列表
        li_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for li in li_list:
            item["book_name"] = li.xpath(".//div[@class='book-title']/a/text()").extract_first()
            item["book_author"] = li.xpath(".//div[@class='book-author']/a/text()").extract_first()
            item["book_publish"] = li.xpath(".//div[@class='book-publish']/a/text()").extract_first()
            item["book-descrip"] = li.xpath(".//div[@class='book-descrip c6']/text()").extract_first()
            item["book_href"] = li.xpath(".//div[@class='book-title']/a/@href").extract_first()

            # 请求具体图书页
            yield scrapy.Request(
                item["book_href"],
                callback= self.detail_book_parse,
                meta={"item":deepcopy(item)}
            )

    def detail_book_parse(self,response):
        # 具体图书详情页
        item = response.meta["item"]
        item["book_price"] = re.findall(r"\"bp\":'(.*?)',",response.body.decode())
        item["book_price"] =  item["book_price"][0] if len( item["book_price"])>0 else None
        print(item)