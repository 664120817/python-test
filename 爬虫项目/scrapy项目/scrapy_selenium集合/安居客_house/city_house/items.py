# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class BeikezufangItem(Item):
    # define the fields for your item here like:
    city = Field()
    region=Field()
    house_name=Field()
    room = Field()
    house_from=Field()
    price=Field()
    url=Field()