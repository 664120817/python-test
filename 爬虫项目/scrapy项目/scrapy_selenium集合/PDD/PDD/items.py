# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class PddItem(Item):
    name = Field()
    price = Field()
    count = Field()
    image_url = Field()



def get_insert_mysql_data(self):
    insert_sql = "INSERT INTO bs('name', 'price', 'count', 'image_url') values (%s,%s,%s,%s,)"
    data = (self['name'], self['price'], self['count'], self['image_url'],)
    print(data)
    return (insert_sql, data)