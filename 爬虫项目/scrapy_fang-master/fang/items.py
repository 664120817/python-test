# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


"""
id 
cityid  440100
cityname 广州。 
distid   区域id  例如BY
distname  distname 白云区
publishtime 发布时间
rentarea 出租面积
roomcnt 几室房 
totalprice  总价 
unitprice 单价
commname  小区名 
"""

class ZFHourseItem(scrapy.Item):
    #id
    id = scrapy.Field()
    # 省份  string
    cityid = scrapy.Field()
    # 区域id string
    distid = scrapy.Field()
    # 发布时间 datetime
    publishtime = scrapy.Field()
    # 出租面积 Float
    rentarea = scrapy.Field()
    #几室房 Bigint
    roomcnt = scrapy.Field()
    # 总价 Float
    totalprice = scrapy.Field()
    # 单价 Float
    unitprice = scrapy.Field()
    # 小区名 string
    commname = scrapy.Field()





