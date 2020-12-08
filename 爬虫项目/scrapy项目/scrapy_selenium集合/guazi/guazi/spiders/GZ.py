# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from guazi.items import GuaziItem
class GzSpider(scrapy.Spider):
    name = 'GZ'
    allowed_domains = ['www.guazi.com']
    star_urls = ['https://www.guazi.com/wh/buy/']


    def start_requests(self):
        url="https://www.guazi.com/wh/siyu/o1/#bread"
        yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        lis=response.css('.carlist.clearfix.js-top li')
        item=GuaziItem()
        for li in lis:
            item['name']= "".join(li.css('.t ::text').extract())
            if item['name'] == None:
                continue
            ages="".join(li.css('.t-i ::text').extract())
            item['age']="".join(re.findall(r'^(\d+)年',ages))
            item['kilometre']="".join(re.findall(r'年\|(.*?)万公里',ages))
            item['serve']="".join(re.findall(r'万公里\|(.*?)$',ages))
            item['price']="".join(li.css('.t-price p::text').extract())
            item['Oprice']="".join(li.css('.line-through::text').extract())
            item['Remarks']="".join(li.css('i ::text').extract())
            yield item
        if response.css('.next'):
            url=response.css('.next ::attr(href)').extract_first()
            print(url)
            yield Request(url=response.urljoin(url),callback=self.parse)

