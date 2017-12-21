# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy


# 让爬虫类继承RedisSpider
class DangdangSpider(RedisSpider):
# class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/'] #由于用的是RedisSpider所以注释掉本行
    redis_key = "dangdang" # redis中的键，值放url

    def parse(self, response):
        # 获取图书分类大列表，切片出有用的标签
        div_list = response.xpath("//div[@class='con flq_body']/div")[2:-1]
        item={}
        for div in div_list:
            # 大分类 ,注意xpath选择语句"./dl/dt//text()"text前面有两个斜杠,同时注意，因为是列表，所以不要extract_first()
            item["b_cate"]= div.xpath("./dl/dt//text()").extract()
            # 中分类列表
            dl_list = div.xpath("./div//dl[@class='inner_dl']")
            # print(dl_list)
            for dl in dl_list:
                # 中分类
                item["m_cate"]= dl.xpath("./dt/a/text()").extract_first()
                # 小分类
                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    # 小分类
                    item["s_cate"]= a.xpath("./@title").extract_first()
                    # 网页详细url
                    item["book_href"]= a.xpath("./@href").extract_first()

                    if item["book_href"] is not None:
                        yield scrapy.Request(
                            item["book_href"],
                            meta={"item":deepcopy(item)},
                            callback=self.parse_detail_book
                        )

    def parse_detail_book(self,resposne):
        # 图书列表详情页
        item = resposne.meta["item"]
        li_list= resposne.xpath("//div[@id='search_nature_rg']/ul/li")
        for li in li_list:
            item["book_name"]= li.xpath("./a/@title").extract_first()
            item["book_img"] = li.xpath("./a/img/@src").extract_first()
            item["book_detail"] = li.xpath("./p[@class='detail']/text()").extract_first()
            item["book_price"] = li.xpath("./p[@class='price']/span[1]/text()").extract_first()
            item["book_comment_count"] = li.xpath("./p[@class='search_star_line']/a/text()").extract_first()
            print(item)

        # 翻页
        next_url_temp = resposne.xpath("//a[text()='下一页']").extract_first()
        if next_url_temp is not None:
            yield scrapy.Request(
                'http://category.dangdang.com'+next_url_temp,
                meta={"item":deepcopy(item)},
                callback=self.parse_detail_book
            )
