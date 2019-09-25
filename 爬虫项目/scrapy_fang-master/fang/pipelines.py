# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import  JsonLinesItemExporter
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors
import json
# from fang.logrecord import *
#装饰器模块


class FangJsonPipeline(object):

    def __init__(self):
        self.newhouse_fp = open('newhouse.json','wb')
        self.esfhouse_fp = open('esfhourse.json','wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp, ensure_ascii=False)

    def process_item(self, item, spider):
        self.newhouse_exporter.export_item(item)
        self.esfhouse_exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()

class FtxPipeline(object):
    def __init__(self):

        dbparams = {
            'host': '47.107.162.55',
            'port': 33306,
            'user': 'root',
            'password': '666666',
            'database': 'scrapy_fang',
            'charset': 'utf8mb4',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

#定义sql
    @property
    def sql(self):  #
        if not self._sql:
            self._sql = """
            insert
            into
            clean_data(id,commid,price_correct,cityid,distid,publishtime,rentarea,roomcnt,totalprice,unitprice,commname)
            values(null,null,null,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql



    def process_item(self,item,spider):
        #把sql的插入语句从同步变成异步
        defer = self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item,spider) #错误处理函数

    def insert_item(self,cursor,item):
        print("数据正在插入数据库")
        #插入数据库语句
        cursor.execute(self.sql,('440100',item['distid'],item['publishtime'],item['rentarea'],item['roomcnt'],item['totalprice'],item['unitprice'],item['commname']))




    #错误处理函数

    def handle_error(self,error,item,spider):  #item 和spider传不传无所谓，传入可以查看是哪里出错了

        print('='*10+'error'+'='*10)
        print(error,item)
        print('='*10+'error'+'='*10)





