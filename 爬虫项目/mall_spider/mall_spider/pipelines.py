# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
实现保存分类的Pipeline类
open_spider方法中，链接MongoDB数据库，获取要操作的集合
process_item方法中，向MongDB中插入类别数据
close_spider方法中，关闭MongDB的链接
"""
from .spiders.jd import JdSpider
from pymongo import MongoClient
class MongDBSpiderPipeline(object):
    def open_spider(self,spider):
        """当爬虫启动的时候执行"""
        if isinstance(spider,JdSpider):
            self.client = MongoClient(host='localhost', port=27017)  # 创建连接对象
            self.collection=self.client.jd.category

    def process_item(self, item, spider):
        #process_item方法中，向MongDB中插入类别数据
        if isinstance(spider,JdSpider):
           self.collection.insert_one(dict(item))
        return item
    def close_spider(self,spider):
        if isinstance(spider, JdSpider):
            self.client.close()

from .spiders.jd_product import JdProductSpider
class ProuctPipeline(object):
    def open_spider(self,spider):
        """当爬虫启动的时候执行"""
        if isinstance(spider,JdProductSpider):
            self.client = MongoClient(host='localhost', port=27017)  # 创建连接对象
            self.collection=self.client.jd.prouct

    def process_item(self, item, spider):
        #process_item方法中，向MongDB中插入类别数据
        if isinstance(spider,JdProductSpider):
           self.collection.insert_one(dict(item))
        return item
    def close_spider(self,spider):
        if isinstance(spider, JdProductSpider):
            self.client.close()