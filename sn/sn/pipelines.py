# -*- coding: utf-8 -*-
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import time
import random
import csv


class SnPipeline(object):

    # mongo客户端
    # def open_spider(self,spider):
    #     client = MongoClient("127.0.0.1", 27017)
    #     self.collection = client["test"]["lianjia"]

    def process_item(self, item, spider):
        # cate_list = []
        # # 文件名字典
        # file_dict = {}
        # if item["s_cate"] is not None:
        #     if item["s_cate"] not in cate_list:
        #         cate_list.append(item["s_cate"])
        #         file_name= '/home/python/Desktop/sn/sn/file_dir/'+item["district"]+item["s_cate"]+'.txt'
        #         file_dict[item["s_cate"]]=file_name
        #     else:
        #         file_name=file_dict[item["s_cate"]]
        #     # 写入文件,用大小分类作为文件名
        #     with open(file_name,'a') as f:
        #         print(item)
                # json.dump(item,f,ensure_ascii=False,indent=2)

        # 以下mongo部分
        # 手动添加集合的_id,不然报错id重复
        # t=str(time.time())
        # t2= random.randint(1000,9999)
        # item["_id"]= t+str(t2)
        # self.collection.insert(item)

        return item


class CSVPipeline(object):

    def __init__(self):
        self.csvfile = open('names.csv', 'w')
        fieldnames = ["s_cate_href", "s_cate", "zone_href", "district", 'house_img', 'house_href', 'house_title','house_desc', 'house_price', 'singel_price', 'house_time', 'house_detail']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)

        return item
