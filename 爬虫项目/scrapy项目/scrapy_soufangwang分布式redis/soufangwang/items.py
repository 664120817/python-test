# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class NewfangwangItem(Item):
    poryince=Field()   #省份
    city=Field()    #城市
    name=Field()   #小区名字
    price=Field()  #价格
    rooms=Field()  #几居室 这个是个列表
    area=Field()   #面积
    address=Field() #地址
    district=Field() #行政区
    sale =Field() #是否在售,类型
    origin_url=Field() #详情页面
class ErsfangwangItem(Item):
    poryince=Field()   #省份
    city=Field()    #城市
    name=Field()   #小区名字
    price=Field()  #价格
    rooms=Field()  #几居室 这个是个列表
    # floor=Field() #朝向
    # year=Field()#年代
    # area=Field()   #面积
    address=Field() #地址
    # unit=Field() #
    # district=Field() #行政区
    origin_url=Field() #详情页面