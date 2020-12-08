# -*- coding: utf-8 -*-
import scrapy
from fang.items import ZFHourseItem
from fang.reflection import region_reflection
from fang.items import ZFHourseItem
from datetime import datetime
import base64,pickle
import re
import time
from io import BytesIO
from fontTools.ttLib import TTFont
from scrapy_redis.spiders import RedisSpider

class SfwSpider(RedisSpider):
    name = 'ajk'
    allowed_domains = ['anjuke.com']
    redis_key = 'ajk:url'
    def make_request_from_data(self,data):
        """
        根据redis中读取的分类信息的二进制数据，构建请求
        :param data:分类信息的二进制数据
        :return:根据小分类URL，构建的请求对象
        """
        #把分类信息的二进制数据 转化为字典
        url=pickle.loads(data)
        #根据小分类的url，构建列表页的请求
        #注意：要使用return来返回一个请求，不要使用yield
        return scrapy.Request(url,callback=self.parse_region)


    #分区域进行解析函数
    def parse_region(self,response):
        base_url = 'https://gz.zu.anjuke.com'
        divs = response.xpath("//div[contains(@class,'zu-info')]")
        # print(type(divs))

        for index, div in enumerate(divs):
            div = divs.xpath("//h3/a/@href").getall()[index]
            yield scrapy.Request(url=div, callback=self.parse_detail)
        next_url = response.xpath("//div[contains(@class,page-content)]/div[contains(@class,multi-page)]/a[@class='aNxt']").get()
        next_url_link = response.xpath("//div[contains(@class,page-content)]/div[contains(@class,multi-page)]/a[contains(@class,'aNxt')]/@href").get()
        # print('next_url',next_url, 'typeof next_url',type(next_url))


        next_url_link = response.xpath(
            "//div[contains(@class,page-content)]/div[contains(@class,multi-page)]/a[contains(@class,'aNxt')]/@href").get()
        print(next_url_link, '!!!!!!!!!!!!!!')
        if next_url_link != None:
            yield scrapy.Request(url=next_url_link, callback=self.parse_region)

    def parse_detail(self,response):
        rentway = response.xpath("//ul[contains(@class,'title-label cf')]/li[contains(@class,'rent')]")
        content = response.xpath("//head/meta[contains(@name,'keywords')]/@content").get()

        secret_key = self.get_bs64_str(response)
        # print(secret_key)
        publishtime = response.xpath("//div[contains(@class,'mod-title')]/div[@class='right-info']/b").get()
        # print(publishtime)
        publishtime = self.get_page_show_ret(publishtime,secret_key)
        publishtime = re.search(".*>(\d+)年(\d+)月(\d+)日</b>",publishtime)
        publishtime = '%s-%s-%s'%(publishtime.group(1),publishtime.group(2),publishtime.group(3))
        publishtime = datetime.strptime(publishtime, '%Y-%m-%d')
        # print(publishtime)

        cityid = '440100'
        cityname = '广州'
        # print(content)
        if "周边" not in content: #排除广州周边小区字段

            text = re.search(r"广州(天河|番禺|白云|海珠|越秀|花都|黄埔|荔湾|增城|南沙|从化|萝岗)(.*?)(\d+)元/月付\d押\d(\d)室.*卫(\d+)平米.*",content)
            try:

                if text.group(1) in region_reflection and int(text.group(4)) < 6:
                    distid= region_reflection[text.group(1)]
                    commname = text.group(2)
                    totalprice = text.group(3)
                    roomcnt = text.group(4)
                    rentarea = text.group(5)
                    unitprice = float(text.group(3)) / float(text.group(5))
                    item = ZFHourseItem(id='null', cityid=cityid,  distid=distid,
                                        publishtime=publishtime, rentarea=rentarea, roomcnt=roomcnt, totalprice=totalprice,
                                        unitprice=unitprice, commname=commname
                                        )
                print(item)
                # yield item
            except:
                pass


    def get_bs64_str(self,response):
        html_str = response.text
        bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", html_str)[0]
        return bs64_str

    def get_page_show_ret(self,mystr, bs64_str):
        '''
        :param mystr: 要转码的字符串
        :param bs64_str:  转码格式
        :return: 转码后的字符串
        '''
        font = TTFont(BytesIO(base64.decodebytes(bs64_str.encode())))
        c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
        ret_list = []
        for char in mystr:
            decode_num = ord(char)
            if decode_num in c:
                num = c[decode_num]
                num = int(num[-2:]) - 1
                ret_list.append(num)
            else:
                ret_list.append(char)
        ret_str_show = ''
        for num in ret_list:
            ret_str_show += str(num)
        return ret_str_show
