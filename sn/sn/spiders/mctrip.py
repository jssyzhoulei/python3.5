# -*- coding: utf-8 -*-
import scrapy
import json
import time
from copy import deepcopy


class MctripSpider(scrapy.Spider):
    name = 'mctrip'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://m.ctrip.com/webapp/hotel/j/hotellistbody?pageid=212093']
    data = {"adultCounts": 0, "checkinDate": "20171209", "checkoutDate": "20171210", "cityID": 2, "cityName": "上海",
            "controlBitMap": 1, "costPerformanceHigh": False, "districtID": 0,
            "domesticHotelList": "domesticHotelList",
            "overseaHotelList": "overseaHotelList", "pageIndex": 1, "pageSize": 10,
            "searchByExposedHotSearchKeyword": False, "searchByExposedZone": False, "showCheckinDate": "12-09",
            "showCheckoutDate": "12-10",  "userLocationSearch": False,
            "validCheckinDate": "20171209"}
    # 构造请求参数
    headers = {'Content-Type': "application/json"}

    def parse(self, response):

        a_list= response.xpath("//a[@class='js_a_seo']")
        if a_list is None:
            return
        for a in a_list:
            item = {}
            item["hotel_title"]= a.xpath("./@title").extract_first()
            item["hotel_img"]= a.xpath(".//img/@src").extract_first()
            item["hotel_scores"]= a.xpath(".//span[@class='c-fn']/b/text()").extract_first()
            item["hotel_count"]= a.xpath(".//div[@class='c-mod']//span[contains(text(),'人点评')]/text()").extract_first()
            item["hotel_district"]= a.xpath(".//span[@class='c-as']/text()").extract_first()
            item["hotel_page_from"]= self.data["pageIndex"]
            item["hotel_href"]= a.xpath("./@href").extract_first()
            if item["hotel_href"] is not None:
                item["hotel_href"]= 'http://m.ctrip.com'+ item["hotel_href"]
                # 请求详情页数据
                yield scrapy.Request(
                    item["hotel_href"],
                    meta={"item":deepcopy(item)},
                    callback=self.parse_detail_info
                )
            # print(item)

        # 请求下一页数据
        # for i in range(2,819):
        #
        #     self.data["pageIndex"] = i
        #     yield scrapy.Request(
        #         self.start_urls[0],
        #         callback=self.parse,
        #         headers=self.headers,
        #         method='post',
        #         body=json.dumps(self.data),
        #     )

    def parse_detail_info(self,response):
        item=response.meta["item"]
        # print(response.text)
        # 房间列表
        li_list= response.xpath("//ul[@class='m-room m-room--tile']/li[@class='item ']")
        # s=re.findall(r'<h3>\w{3}</h3>',response.text)[0]
        # print(s)
        for li in li_list:
            item["house_style"]= li.xpath(".//div[@class='room-bd']/h3/text()").extract_first()
            item["house_size"]=[]
            size = li.xpath(".//div[@class='room-bd']/p[@class='room-size']/em")
            for si in size:
                info=si.xpath("./text()").extract_first()
                item["house_size"].append(info)
            print(item)

    def start_requests(self):

        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            headers=self.headers,
            method='post',
            body=json.dumps(self.data)
        )