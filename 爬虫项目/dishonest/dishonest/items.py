# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
"""
根据需求，定义数据模型
步骤：
1，定义数据模型类：DishonestItem,，继承scrapy.Item
2,定义要抓取字段
失信人名称 ，号码，年龄，区域，法人（企业），失信内容 ，公布日期，公布/执行单位
创建日期 更新日期
"""
import scrapy
from scrapy import Item,Field

class DishonestItem(Item):
    name=Field()# 失信人名称
    sexy=Field()# 性别
    age = Field()# 年龄,企业年龄都为0
    card_num = Field()  # 号码
    area= Field()# 区域
    business_entity = Field()# 法人（企业）
    content = Field()# 失信内容
    publish_date = Field()# 公布/宣判日期
    publish_unit = Field()# 公布 / 执行单位
    # create_date = Field()# 创建日期
    update_date = Field()# 更新日期