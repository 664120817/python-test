# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class GuaziItem(Item):

    name = Field()
    age = Field()
    kilometre = Field()
    serve = Field()
    price = Field()
    Oprice = Field()
    Remarks = Field()

