# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class JianshuPipeline(object):
    def process_item(self, item, spider):
        return item


class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user':'root',
            'password':'4786874',
            'database':'jianshu_selenium',
            'charset': 'utf8',
            'cursorclass':cursors.DictCursor, #指定游标


        }
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams) #填写链接的数据库
        self._sql =None
    @property
    def sql(self):
        if not self._sql :
            self._sql  =  """
            INSERT INTO js(title,dz,date,user_url,text) VALUES (%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql
    def process_item(self,item,spider):
        defer =self.dbpool.runInteraction(self.insert_item ,item) #数据插入
        defer.addErrback(self.handle_error,item,spider)  #报错


    def insert_item(self,cursor,item):  #异步插入数据

        cursor.execute(self.sql,(item['title'], item['dz'],item['date'],item['user_url'], item['text']))
        return item

    def handle_error(self,error,item,spider):  #报错提示
        print("错误：",error)