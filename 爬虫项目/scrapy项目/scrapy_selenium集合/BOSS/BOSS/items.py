# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Item,Field

class BossItem(Item):
    # define the fields for your item here like:
    name = Field()
    salary = Field()
    ed = Field()
    company_name = Field()
    address = Field()
    position = Field()
    url =Field()

    #按住ALT键

    def get_insert_mysql_data(self):
        insert_sql ="INSERT INTO bs(name,salary,ed,company_name,address,position,url) values (%s,%s,%s,%s,%s,%s,%s)"

        data =(self['name'],self['salary'],self['ed'],self['company_name'],self['address'],self['position'],self['url'],)
        print(data)
        return (insert_sql,data)