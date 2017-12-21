# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider

class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    redis_key = "amazon"

    rules = (
        #提取小分类的url地址 #提取图书列表页的地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='categoryRefinementsSection']/ul/li",)), follow=True),
        #提取图书详情页的地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']//h2/..",)), callback="parse_item",follow=False),
    )

    def parse_item(self, response):  #提取图书的信息
        item = {}
        #分类信息
        item["cate_list"] = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']/ul/li[not(@class='a-breadcrumb-divider')]/span/a/text()").extract()
        item["cate_href_list"] = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']/ul/li[not(@class='a-breadcrumb-divider')]/span/a/@href").extract()
        item["cate_href_list"] = ["https://www.amazon.cn"+i for i in item["cate_href_list"]]
        #图书的标题
        item["book_title_info"] = response.xpath("//title/text()").extract_first()
        #是否为电子书
        item["is_ebook"] = False
        if "Kindle电子书" in item["book_title_info"]:
            item["is_ebook"] = True
        #获取作者信息
        item["book_authors"] = []
        span_list = response.xpath("//span[@class='author notFaded']")
        for span in span_list:
            author = {}
            author["name"] = span.xpath("./a/text()").extract_first()
            author["info"] = span.xpath("./span/span/text()").extract_first()
            item["book_authors"].append(author)
        #获取商品的评价数量
        item["book_comments_num"] = response.xpath("//span[@id='acrCustomerReviewText']/text()").extract_first()
        #获取图书价格
        if item["is_ebook"]:
            item["book_price"] = response.xpath("//tr[@class='kindle-price']/td[2]/text()").extract_first()

        else:
            item["book_price"] = response.xpath("//div[@id='soldByThirdParty']/span[2]/text()").extract_first()
        # 获取图片
        # item["book_img"] = response.xpath("//div[contains(@id,'img-canvas')]/img/@src").extract_first()

        #获取出版社
        item["book_press"] = response.xpath("//b[text()='出版社:']/../text()").extract_first()

        print(item)
