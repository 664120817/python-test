# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class JianshuItem(Item):
    title = Field()
    user_url = Field()
    date = Field()
    dz = Field()
    text = Field()

