# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from openpyxl import Workbook
class ExcelPipeline(object):
    def __init__(self):
        #创建excel,填写表头
        self.wb=Workbook()
        self.ws=self.wb.active
        self.ws.append(["型号名","现价","原价","行驶里程","使用年限","服务","备注"])

    def process_item(self, item, spider):
        line=[item["name"],item["price"],item["Oprice"],item["kilometre"],item["age"],item["serve"],item["Remarks"]]
        self.ws.append(line)
        self.wb.save("思域.xlsx")
        return item
