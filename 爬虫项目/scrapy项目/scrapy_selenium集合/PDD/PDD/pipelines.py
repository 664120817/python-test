# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

# class PddPipeline(object):
#     def process_item(self, item, spider):
#         return item

class ExcelPipeline(object):
    def __init__(self):
        # 创建excel,填写表头
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["price", "count","name","image_url" ])

    def process_item(self, item, spider):

            line = [ item['price'], item['count'],item['name'], item['image_url']]
            self.ws.append(line)
            self.wb.save("简奈妮旗舰店.xlsx")

            return item

import pymysql
class MysqlPipeline(object):
    def __init__(self):
        self.db = pymysql.Connect(host="localhost", db="spider",
                                  charset="utf8mb4")
        # 获取操作数据库的cursor
        self.cursor = self.db.cursor()
    def process_item(self, item, spider):
        print("6666666666")
        if 'get_insert_mysql_data' in dir(item): #判断这个函数是否属于这个类里
            (insert_sql,data) = item.get_insert_mysql_data()
            print(data)
            # 执行SQL
            self.cursor.execute(insert_sql, data)
            # 提交事务
            self.db.commit()

        return item