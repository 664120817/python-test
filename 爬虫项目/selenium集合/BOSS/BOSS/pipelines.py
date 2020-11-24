# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class BossPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def __init__(self):
        self.db = pymysql.Connect(host="localhost", port=3306, user="root", passwd="4786874", db="spider",
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