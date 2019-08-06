# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ZhihuItem(Item):
    id=Field()
    name=Field()
    url=Field()
    url_token=Field()
