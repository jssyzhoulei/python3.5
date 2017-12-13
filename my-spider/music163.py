import requests
from lxml import etree
from copy import deepcopy
from selenium import webdriver
from pprint import pprint


class music163:
    def __init__(self):
        self.start_url = 'http://music.163.com/discover/playlist/?cat=%E5%8D%8E%E8%AF%AD'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    def parse_url(self,url):
        # 请求资源
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_category_list(self,response):
        # 获取大小分类信息
        html = etree.HTML(response)
        # 解析获取数据
        dl_list = html.xpath("//div[@id='cateListBox']/div[@class='bd']/dl")
        category_list =[]
        for dl in dl_list:
            b_cate=dl.xpath("./dt/text()")[0] if len(dl.xpath("./dt/text()"))>0 else None
            a_list = dl.xpath("./dd/a")
            for a in a_list:
                item={}
                item["b_cate"]= b_cate
                item["s_cate"]= a.xpath("./text()")[0] if len(a.xpath("./text()"))>0 else None
                item["s_cate_href"] =a.xpath("./@href")[0] if len(a.xpath("./@href"))>0 else None
                if item["s_cate_href"] is not None:
                    item["s_cate_href"]= 'http://music.163.com'+ item["s_cate_href"]
                category_list.append(item)
        return category_list

    def get_playlist_list(self, playlist,total_playlist):
        # 获取歌单列表页歌单列表
        if playlist is not None:
            html= self.parse_url(playlist["s_cate_href"])
            html=etree.HTML(html)
            li_list= html.xpath("//ul[@id='m-pl-container']/li")
            # 创建一个空的歌单列表的列表
            playlist_list=[]
            for li in li_list:
                # 歌单信息
                playlist["play_list_title"]= li.xpath("./p[1]/a/text()")[0] if len(li.xpath("./p[1]/a/text()")) else None
                playlist["play_list_href"] = li.xpath("./p[1]/a/@href")[0] if len(li.xpath("./p[1]/a/@href")) else None
                if playlist["play_list_href"] is not None:
                    playlist["play_list_href"]= 'http://music.163.com' + playlist["play_list_href"]
                playlist["play_list_author"]= li.xpath("./p[2]/a/@title")[0] if len(li.xpath("./p[2]/a/@title")) else None
                playlist["play_list_comment"]= li.xpath("./div/div/span[2]/text()")[0] if len(li.xpath("./div/div/span[2]/text()")) > 0 else None
                # 把当前歌单列表添加到大列表,注意深拷贝
                playlist_list.append(deepcopy(playlist))
            # pprint(playlist_list)
            # 把当前页的歌单大列表添加到歌单总列表,用作传递到递归的函数中
            total_playlist.extend(playlist_list)

            # 下一页的地址
            next_url=html.xpath("//a[text()='下一页']/@href")[0] if len(html.xpath("//a[text()='下一页']/@href"))>0 else None
            if next_url is not None and next_url!= 'javascript:void(0)':
                next_url= 'http://music.163.com'+next_url
                # 把下一页赋值给小分类href
                playlist["s_cate_href"]= next_url
                print("*"*100,next_url)
                # 递归调用自身
                return self.get_playlist_list(playlist,total_playlist)
        return total_playlist

    def parse_detail_playlist(self,playlist):
        if playlist["play_list_href"] is not None:
            html=self.parse_url(playlist["play_list_href"])
            # 解析详情页的数据
            html= etree.HTML(html)
            playlist["fav_count"]= html.xpath("//a[@data-res-action='fav']/@data-count")[0] if len(html.xpath("//a[@data-res-action='fav']/@data-count"))>0 else None
            playlist["playlist_comment"]= html.xpath("//span[@id='cnt_comment_count']/text()")[0] if len(html.xpath("//span[@id='cnt_comment_count']/text()"))>0 else None
            playlist["playlist_introduce"]= html.xpath("//p[@id='album-desc-dot']/text()") if len(html.xpath("//p[@id='album-desc-more']/text()"))>0 else None
            playlist["track_list"]= self.get_playlist_tracks(playlist["play_list_href"])
            pprint(playlist)

    def get_playlist_tracks(self,url):
        # 获取每个歌单列表的每首歌曲详细信息
        track_list=[]
        web= webdriver.Chrome()
        web.get(url)
        # 切换到frame中
        web.switch_to.frame("g_iframe")
        html= web.page_source
        html= etree.HTML(html)
        web.quit()
        tr_list= html.xpath("//tbody/tr")
        for tr in tr_list:
            # 遍历歌曲
            item={}
            item["track_name"]= tr.xpath(".//a/b/text()")[0] if len(tr.xpath(".//a/b/text()"))>0 else None
            item["track_duration"]=tr.xpath("./td/span[@class='u-dur ']/text()")[0] if len(tr.xpath("./td/span[@class='u-dur ']/text()"))>0 else None
            item["track_author"]= tr.xpath("./td[4]/div/@title")[0] if len(tr.xpath("./td[4]/div/@title"))>0 else None
            item["track_col"]= tr.xpath("./td[5]/div/a/@title")[0] if len(tr.xpath("./td[5]/div/a/@title"))>0 else None
            track_list.append(item)
        return track_list

    def run(self):
        # start_url　请求163资源响应
        html = self.parse_url(self.start_url)
        # 获取分类列表
        category_list= self.get_category_list(html)
        for category in category_list:
            total_playlist=self.get_playlist_list(category,[])
            # 列表中的每一个播放列表
            for playlist in total_playlist:
                self.parse_detail_playlist(playlist)


if __name__ == '__main__':
    music= music163()
    music.run()