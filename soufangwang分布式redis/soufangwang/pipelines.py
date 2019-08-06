# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from soufangwang.items import NewfangwangItem,ErsfangwangItem

class SoufangwangPipeline(object):
    def __init__(self):
        self.newhouse_fp=open("newhouse.json","wb")
        self.esfhouse_fp=open("esfhouse.json","wb")
        self.newhouse_exporter=JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp, ensure_ascii=False)
    def process_item(self, item, spider):
        if isinstance(item,NewfangwangItem):
           self.newhouse_exporter.export_item(item)
        if isinstance(item, ErsfangwangItem):
           self.esfhouse_exporter.export_item(item)
        return item
    def close_Spider(self,spider):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()

from openpyxl import Workbook
class ExcelPipeline(object):
    def __init__(self):
        #创建excel,填写表头
        self.wb=Workbook()
        self.ws=self.wb.active
        self.ws.append(["省份", "城市", "小区名字", "价格", "居室", "面积", "行政区", "地址", "是否在售or类型", "origin_url"])
        # self.WB = Workbook()
        self.wl= self.wb.active
        self.wl.append(["省份", "城市", "小区名字", "价格", "居室", "地址", "origin_url"])
    def process_item(self, item, spider):

        # if isinstance(item,NewfangwangItem):
        #     line=[item['poryince'],item['city'],item['name'],item['price'],item['rooms'],item['area'],item['district'],item['address'],item['sale'],item['origin_url']]
        #     self.ws.append(line)
        #     self.wb.save("武汉新盘.xlsx")
        if isinstance(item,ErsfangwangItem):
            lines = [item['poryince'], item['city'], item['name'], item['price'], item['rooms'],item['address'],item['origin_url']]
            self.wl.append(lines)
            self.wb.save("武汉二手房.xlsx")
        return item

import csv,os
class Pipeline_ToCSV(object):

    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/武汉新房.csv'
        store_files = os.path.dirname(__file__) + '/spiders/武汉二手房.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'w')
        # csv写法
        self.writer = csv.writer(self.file)
        self.writer.writerow(("省份", "城市", "小区名字", "价格", "居室", "面积", "行政区", "地址", "是否在售or类型", "origin_url"))
        self.files=open(store_files, 'w')
        self.writers = csv.writer(self.files)
        self.writers.writerow(("省份", "城市", "小区名字", "价格", "居室", "地址", "origin_url"))

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        if isinstance(item, NewfangwangItem):
            self.writer.writerow((item['poryince'],item['city'],item['name'],item['price'],item['rooms'],item['area'],item['district'],item['address'],item['sale'],item['origin_url']))
        if isinstance(item, ErsfangwangItem):
            self.writers.writerow((item['poryince'], item['city'], item['name'], item['price'], item['rooms'],item['address'],item['origin_url']))
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
        self.files.close()


