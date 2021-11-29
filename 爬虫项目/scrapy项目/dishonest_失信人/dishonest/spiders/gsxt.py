# -*- coding: utf-8 -*-
import scrapy,json,re,datetime
from dishonest.items import DishonestItem


class GsxtSpider(scrapy.Spider):
    name = 'gsxt'
    allowed_domains = ['gsxt.gov.cn']
    start_urls = ['http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html']

    data_url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid=100000&noticeTitle=&regOrg={}'

    def parse(self, response):
        # print(response.status, "666")
        # print(response.text)
        # 获取包含省/直辖市的名称和ID
        divs=response.css('.label-list  div')
        for div in divs:
            area=div.css('div label::text').extract_first()
            id=div.css('div::attr(id)').extract_first()
            # print(area,id)
            data_url= self.data_url.format(id)
            # print(data_url)
            for page in range(0,50,10):
                data={

                    'start': str(page),
                    'length': '10',
                }
                yield scrapy.FormRequest(data_url,formdata=data,callback=self.parse_data,meta={'area':area})
    def parse_data(self,response):
        area=response.meta['area']
        #把JOSN 字符串转化成字典
        response=json.loads(response.text)
        datas=response['data']
        # 遍历datas，获取每一个公告信息：
        for data in datas:
            item =DishonestItem()
            #获取通知标题
            notice_title =data['noticeTitle']
            #获取通知内容
            notice_content=data['noticeContent']
            names=re.findall(r'关?于?(.*?)的?列入.*',notice_title)
            item['name'] = names[0]  if len(names) != 0 else "" # 失信人名称
            name_card_num_s=re.findall(r'经?查?，?(.*?)\s*（统一社会信用代码/注册号：(\w+)）：.*',notice_content)
            if len(name_card_num_s) != 0:
                if item['name'] == None:
                   item['name'] = name_card_num_s[0][0]
                item['card_num'] = name_card_num_s[0][1]
            item['sexy'] = "企业"  # 性别
            item['age'] = 0  # 年龄都是企业年龄都为0
            item['area'] = area  # 区域
            item['business_entity'] = "空"  # 法人（企业）
            item['content'] = notice_content  # 失信内容
            publish_ms = data['noticeDate']  # 公布/宣判日期
            publish_date = datetime.datetime.fromtimestamp(publish_ms / 1000)
            item['publish_date'] = publish_date.strftime('%Y-%m-%d')
            item['publish_unit'] = data['judAuth_CN']  # 公布 / 执行单位
            # item['create_date'] =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建日期
            item['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 更新日期
            yield item


            



