# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://shanghai.anjuke.com/sale/']

    def parse(self, response):
        # 获取小分类地址
        a_list = response.xpath("//div[@class='items']/span[@class='elems-l']/a[not(@rel)]")
        for a in a_list:
            item={}
            item["district"]= a.xpath("./text()").extract_first()
            item["cate_href"]= a.xpath("./@href").extract_first()
            # print(item)
            if item["cate_href"] is not None:
                # 构建详情页请求
                yield scrapy.Request(
                    item["cate_href"],
                    callback=self.parse_list_info,
                    meta={"item":deepcopy(item)}
                )

    def parse_list_info(self,response):
        # 列表页数据
        item= response.meta["item"]
        # 房产列表
        li_list= response.xpath("//ul[@id='houselist-mod-new']/li")
        # print(li_list)
        for li in li_list:
            item={}
            item["house_title"]= li.xpath(".//div[@class='house-title']/a/text()").extract_first()
            item["house_href"]= li.xpath(".//div[@class='house-title']/a/@href").extract_first()
            item["house_href"]= li.xpath(".//div[@class='item-img']/img/@src").extract_first()
            span_list= li.xpath(".//div[@class='details-item']/span")
            item["house_detail"]= []
            for span in span_list:
                detail= span.xpath("./text()").extract_first()
                item["house_detail"].append(detail)
            item["house_addr"]= li.xpath(".//span[@class='comm-address']/text()").extract_first()
            if item["house_addr"] is not None:
                item["house_addr"]=item["house_addr"].strip()
            span_list= li.xpath(".//div[@class='tags-bottom']/span")
            item["house_tags"]=[]
            for div in span_list:
                tags= div.xpath("./text()").extract_first()
                item["house_tags"].append(tags)
            item["house_price"]= li.xpath(".//span[@class='price-det']/strong/text()").extract_first()
            print(item)

        # 请求下一页数据
        next_url = response.xpath(".//a[@text()='下一页']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse_list_info,
                meta={"item":deepcopy(item)}
            )