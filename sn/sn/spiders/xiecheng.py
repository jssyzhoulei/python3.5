# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json
import time


class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://hotels.ctrip.com/hotel/shanghai2/']

    def parse(self, response):
        div_list = response.xpath("//div[@id='hotel_list']/div")[:-1]
        for div in div_list:
            item = {}
            item["hotel_title"] = div.xpath(".//div[@class='hotel_pic']/a/@title").extract_first()
            item["hotel_img"] = div.xpath(".//div[@class='hotel_pic']/a/img/@src").extract_first()
            hotel_span= div.xpath(".//span[@class='hotel_ico']/span")
            item["hotel_dec"]=[]
            for span in hotel_span:
                text= span.xpath("./@title").extract_first()
                item["hotel_dec"].append(text)
            item["hotel_comment"]=[]
            span_list= div.xpath(".//div[@class='hotelitem_judge_box']/a/span")
            for span in span_list:
                text= span.xpath("./text()").extract_first()
                item["hotel_comment"].append(text)
            item["hotel_href"]= div.xpath(".//h2[@class='hotel_name']/a/@href").extract_first()
            # print(item)
            if item["hotel_href"] is not None:
                item["hotel_href"]= 'http://hotels.ctrip.com'+item["hotel_href"]
                time.sleep(1)
                # 请求详情页信息
                scrapy.Request(
                    item["hotel_href"],
                    callback=self.parse_detail_info,
                    meta={"item":deepcopy(item)}
                )

        # 获取下一页url
        # next_url='http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
        # data = 'StartTime:2017-12-07,DepTime:2017-12-08,cityId:2,page:381'
        # data = {i.split(":")[0]: i.split(":")[-1] for i in data.split(',')}
        # for i in range(384):
        #     data["page"]=str(i)
        #     yield scrapy.FormRequest(
        #         next_url,
        #         callback=self.parse_next_url,
        #         formdata=data
        #     )

    # 详情页解析函数
    def parse_detail_info(self,response):
        item= response.meta["item"]
        tr_list= response.xpath("//table/tbody/tr[@data-disable]")
        print(tr_list)
        for tr in tr_list:
            item["room_type"]= tr.xpath("./td/a[@class='room_unfold']/text()").extract_first()
            item["bed_type"]= tr.xpath("./td[@class='col3']").extract_first()
            item["breakfast"]= tr.xpath("./td[@class='col4']").extract_first()
            item["room_wifi"]= tr.xpath("./td[@class='col5']/span/text()").extract_first()
            item["person_limit"]= tr.xpath("./td[@class='col_person']/span/@title").extract_first()
            print(item)


    def parse_next_url(self,response):
        # 取出json格式响应字符串,text属性
        json_response=response.text
        r= json.loads(json_response)
        for info in r["hotelPositionJSON"]:
            item={}
            item["hotel_title"]= info["name"]
            item["hotel_img"]= info["img"]
            item["hotel_dec"]= info["stardesc"]
            item["hotel_comment"] = []
            item["hotel_comment"].append("住客点评量"+info["dpcount"])
            item["hotel_comment"].append("评分"+info["score"])
            item["address"]=info["address"]
            item["hotel_href"]= 'http://hotels.ctrip.com/hotel/{}.html'.format(info["id"])
            print(item)