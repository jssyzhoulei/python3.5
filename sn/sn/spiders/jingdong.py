# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # 获取京东图书页大分类
        dt_list = response.xpath("//div[@id='booksort']/div[2]/dl/dt")
        for dt in dt_list:
            item={}
            item["b_cate"] = dt.xpath("./a/text()").extract_first()
            # 获取小分类列表
            dd_list = dt.xpath("./following-sibling::*[1]/em")
            for dd in dd_list:
                # 小分类
                item["s_cate"]= dd.xpath("./a/text()").extract_first()
                # 小分类的url
                item["s_href"] = dd.xpath("./a/@href").extract_first()
                item["s_href"] = 'https:'+ item["s_href"] if len( item["s_href"])>0 else None
                # 请求详情页
                yield scrapy.Request(
                    item["s_href"],
                    callback=self.book_list_parse,
                    meta={"item":deepcopy(item)}
                )

    def book_list_parse(self,response):
        # 提取详情页的信息
        item=response.meta["item"]
        # 获取图书列表
        li_list = response.xpath("//ul[@class='gl-warp clearfix']/li")
        for li in li_list:
            item["book_name"] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item["book_img"] = li.xpath(".//div[@class='p-img']/a/img/@src|.//div[@class='p-img']/a/img/@data-lazy-img").extract_first()
            item["book_href"] = li.xpath(".//div[@class='p-img']/a/@href").extract_first()
            if item["book_href"] is not None:
                item["book_href"]='https:' + item["book_href"]
            item["book_author"] = li.xpath(".//span[@class='author_type_1']/a/@title").extract_first()
            item["book_press"] = li.xpath(".//span[@class='p-bi-store']/a/@title").extract_first()
            # 获取图书sku编码的字符串格式
            sku = li.xpath(".//div[@class='gl-i-wrap j-sku-item']/@data-sku").extract_first()

            # 请求价格信息
            yield scrapy.Request(
                "https://p.3.cn/prices/mgets?skuIds={}".format(sku),
                callback=self.parse_book_price,
                meta={"item":deepcopy(item)}
            )
            # print(item)

        next_url_temp= response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url_temp is not None:
            # 请求下一页信息
            next_url = 'https://list.jd.com'+next_url_temp
            yield scrapy.Request(
                next_url,
                meta={"item":deepcopy(item)},
                callback=self.book_list_parse
            )

    def parse_book_price(self,response):
        # 解析价格数据
        item= response.meta["item"]
        # 获取json格式响应
        json_response = response.body.decode()
        if json_response is not None:
            item["book_price"] = json.loads(json_response)[0]["op"]
        print(item)

