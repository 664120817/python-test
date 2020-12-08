# -*- coding: utf-8 -*-
import scrapy,json,datetime
from jsonpath import jsonpath

from dishonest.items import DishonestItem
class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    # 起始URL：'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E4%BA%BA&pn=20&rn=10&ie=utf-8&oe=utf-8'
    start_urls = ['https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E4%BA%BA&pn=20&rn=10&ie=utf-8&oe=utf-8']

    def parse(self, response):
        #构建所有页面请求
        #把响应内容的json字符串，转化为字典
        response=json.loads(response.text)
        #取出总数据条数
        dip_pum=jsonpath(response,'$..dispNum')[0]
        #每隔10条数据，构建一个请求
        url_pattern='https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E4%BA%BA&pn={}&rn=10&ie=utf-8&oe=utf-8'
        for pn in range(0,dip_pum,10):
            #构建URL
            url=url_pattern.format(pn)
            yield scrapy.Request(url,callback=self.parse_data)
    def parse_data(self,response):
        #解析数据
        datas=json.loads(response.text)
        results=jsonpath(datas,'$..result')[0]
        #遍历结果列表
        for res in results:
            item=DishonestItem()
            item['name'] = res['iname']  # 失信人名称
            item['sexy'] =res['sexy'] #性别
            item['card_num'] = res['cardNum']  # 号码
            item['age'] =int(res['age'])  # 年龄,企业年龄都为0
            item['area'] = res['areaName']  # 区域
            item['business_entity'] = res['businessEntity']  # 法人（企业）
            item['content'] = res['duty']  # 失信内容
            item['publish_date'] = res['publishDate']  # 公布/宣判日期
            item['publish_unit'] = res['courtName']  # 公布 / 执行单位
            # item['create_date'] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建日期
            item['update_date'] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 更新日期
            yield item