# -*- coding: utf-8 -*-
import scrapy,json,datetime

from dishonest.items import DishonestItem
"""
1,完善爬虫
2，构建起始URL
3，获取总页数，构建所有页面请求
4，解析页面数据
"""
class CourtSpider(scrapy.Spider):
    name = 'court'
    allowed_domains = ['court.gov.cn']
    # start_urls = ['http://court.gov.cn/']
    post_url='http://jszx.court.gov.cn/api/front/getPublishInfoPageList'
    #构建起始请求
    def start_requests(self):
        data ={
            'pageSize': '10',
            'pageNo': '1'
        }
        #构建POST请求，交给引擎
        yield scrapy.FormRequest(self.post_url,formdata=data,callback=self.parse)

    def parse(self, response):
        # 将json字符串 转化字典
        response=json.loads(response.text)
        #解析页面获取总页数
        pages=response['pageCount']
        #构建每一个请求
        for page in range(pages):
            data = {
                'pageSize': '10',
                'pageNo': str(page)
            }
            yield scrapy.FormRequest(self.post_url,formdata=data,callback=self.data_parse)
    def data_parse(self,response):
        response = json.loads(response.text)
        #解析数据
        datas=response['data']
        for data in datas:
            item = DishonestItem()
            item['name'] = data['name']  # 失信人名称
            item['sexy'] = 'court'  # 性别
            item['card_num'] = data['cardNum']  # 号码
            item['age'] = int(data['age'])  # 年龄,企业年龄都为0
            item['area'] = data['areaName']  # 区域
            item['business_entity'] = data['buesinessEntity']  # 法人（企业）
            item['content'] = data['duty']  # 失信内容
            item['publish_date'] = data['publishDate']  # 公布/宣判日期
            item['publish_unit'] = data['courtName']  # 公布 / 执行单位
            # item['create_date'] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建日期
            item['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 更新日期
            yield item
            # print(item)


