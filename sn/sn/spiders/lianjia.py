# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
from pprint import pprint
import re


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://sh.lianjia.com/ershoufang/']
    # redis_key = 'lianjia'

    def parse(self, response):
        # 区域列表
        a_list= response.xpath("//div[@id='plateList']/div/a")[1:]

        for a in a_list:
            item={}
            item["district"]= a.xpath("./@title").extract_first()
            item["zone_href"]= a.xpath("./@href").extract_first()
            if item["zone_href"] is not None:
                item["zone_href"]= 'http://sh.lianjia.com'+item["zone_href"]
                # pprint(item)
                # 请求小分类数据

                yield scrapy.Request(
                    item["zone_href"],
                    meta={"item":deepcopy(item)},
                    callback=self.parse_s_cate

                )

    def parse_s_cate(self,response):
        # 解析出中分类的数据
        item= response.meta["item"]
        div_list=response.xpath("//div[@id='plateList']/div[@class='level2 gio_plate']/div")[1:]
        for div in div_list:
            item["s_cate"]= div.xpath("./a/text()").extract_first()
            item["s_cate_href"]= div.xpath("./a/@href").extract_first()
            # pprint(item)
            if item["s_cate_href"] is not None:
                item["s_cate_href"]= 'http://sh.lianjia.com'+item["s_cate_href"]

                # 请求具体数据
                yield scrapy.Request(
                    item["s_cate_href"],
                    meta={"item":deepcopy(item)},
                    callback=self.parse_detail_info
                )

    def parse_detail_info(self,response):
        item=response.meta["item"]
        # 提取具体信息
        li_list = response.xpath("//ul[@class='js_fang_list']/li")
        # 每套二手房
        for li in li_list:
            item["house_img"]= li.xpath("./a/img/@data-img-real").extract()
            # item["house_img"]= re.findall('(.*?)_\d+x\d+.jpg',item["house_img"])[0]
            item["house_href"]= li.xpath("./a/@href").extract_first()
            if item["house_href"] is not None:
                item["house_href"]= 'http://sh.lianjia.com'+item["house_href"]

            item["house_title"]= li.xpath("./div[@class='info']/div[1]/a/@title").extract()
            item["house_desc"]= li.xpath(".//div[@class='info-table']/div[1]/span/text()").extract()
            item["house_desc"]= [re.sub(r'\s+',"",i) for i in item["house_desc"]]
            item["house_desc"]= [i for i in item["house_desc"] if len(i)>0]
            item["house_price"]= li.xpath(".//div[@class='info-col price-item main']/span[1]/text()").extract()
            item["singel_price"]= li.xpath(".//div[@class='info-table']/div[2]/span[2]/text()").extract()
            item["singel_price"] =[ i.strip() for i in item["singel_price"] if item["singel_price"] is not None]

            # item["singel_price"] = item["singel_price"].strip() if item["singel_price"] is not None else None

            item["house_time"]= li.xpath(".//span[@class='info-col row2-text']/text()").extract()
            item["house_time"]= [re.sub(r'\s+|\|',"",i) for i in item["house_time"]]
            item["house_time"]= [i for i in item["house_time"] if len(i)>0]
            item["house_detail"] = li.xpath(".//span[@class='info-col row2-text']/a[@class='laisuzhou']/span/text()").extract()
            pprint(response.request.meta['proxy'])
            # print(item)
            yield item
