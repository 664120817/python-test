# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class MysqlPipeline(object):
    def open_spider(self,spider):
        # self.db = pymysql.Connect(host="localhost", port=3306, user="", passwd="", db="spider", charset="utf8mb4")
       
        #获取操作数据库的cursor
        self.cursor=self.db.cursor()

    def process_item(self, item, spider):
    #     select_count_sql = "SELECT COUNT(1) from mtcy WHERE 电话 ='{}'".format(item['电话'])
    #     # 执行查询SQL
    #     self.cursor.execute(select_count_sql)
    #     # 获取查询结果
    #     count = self.cursor.fetchone()[0]
    #     print(count)
    #     if count == True:
    #         sql = "delete from mtcy where 电话 ='{}'".format(item['电话'])
    #         self.cursor.execute(sql)
    #         self.db.commit()
    #     select_count_sql = "SELECT COUNT(1) from mtcy WHERE 电话 ='{}'".format(item['电话'])
    #     # 执行查询SQL
    #     self.cursor.execute(select_count_sql)
    #     # 获取查询结果
    #     count = self.cursor.fetchone()[0]
    #     if count == 0:
        keys, values = zip(*dict(item).items())  # dict(item).items()整合成列表性元组，zip拆分列表成各个元组，keys,values接收元组的键和值
        print(len(keys), len(values), 888888)
        # 如果没有数据，就插入数据
        insert_sql = 'INSERT INTO bkzf ({}) VALUES ({})'.format(','.join(keys), ','.join(['%s'] * len(keys)))

        print(insert_sql, 666666666)
        # 执行SQL
        self.cursor.execute(insert_sql, values)
        # 提交事务
        self.db.commit()
        return item

    def close_spider(self,spider):
        #在close_spider中，关闭cursor,关闭数据库连接
        # 1，先关闭cursor
        self.cursor.close()
        #2,在关闭数据库连接
        self.db.close()