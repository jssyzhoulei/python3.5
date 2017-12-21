# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class DazhongSpider(scrapy.Spider):
    name = 'dazhong'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/search/category/1/10/g110']

    def parse(self, response):
        # 商家列表
        li_list= response.xpath("//div[@id='shop-all-list']/ul/li[not(@data-viewed)]")
        for li in li_list:
            item={}
            item["title"]= li.xpath(".//div[@class='tit']/a/@title|.//div[@class='tit']/a[1]/@title").extract_first()
            item["img"]= li.xpath("./div[@class='pic']/a/img/@data-src").extract_first()
            item["img"] = item["img"].split("%")[0] if len(item["img"])>0 else None
            item["desc"]= li.xpath("./div[@class='svr-info']//a/@title").extract()
            # item["desc"]= item["desc"][0] if len(item["desc"][0])>0 else item["desc"][1]
            item["comment_count"]= li.xpath(".//a[@class='review-num']/b/text()").extract_first()
            span_list= li.xpath(".//span[@class='comment-list']/span")
            item["scores"]=''
            for span in span_list:
                tag= span.xpath("./text()").extract_first()
                score=span.xpath("./b/text()").extract_first()
                item["scores"]+=(tag+score)
            item["detail_addr"]= li.xpath(".//div[@class='tag-addr']/span/text()").extract_first()
            item["district"]= li.xpath(".//div[@class='tag-addr']/a[2]/span/text()").extract_first()
            print(item)

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )