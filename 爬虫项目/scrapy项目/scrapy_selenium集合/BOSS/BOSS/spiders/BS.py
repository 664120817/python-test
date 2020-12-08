# -*- coding: utf-8 -*-
import scrapy
from BOSS.items import BossItem

class BsSpider(scrapy.Spider):
    name = 'BS'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/c101200100/?query=python&page=1&ka=page-1']
    # url = "https://www.zhipin.com/c101020100/?query=python&page={}&ka=page-{}"
    #
    # def start_requests(self):
    #     yield scrapy.Request(url = self.url.format(1,1),
    #                   callback=self.parse)


    def parse(self, response):
        urls = response.css(".job-name a::attr(href)").getall()
        for url in urls:
            url ="https://www.zhipin.com/" +str(url)
            print(url)
            yield scrapy.Request(url=url,callback=self.parse_show,meta={"url":url})
        print(response.css('.page .page-cur::text').get())
        if response.css('.page .next::text').get() == None :
            url = response.css('.page .next::attr(href)').get()
            print(url)
            url ="https://www.zhipin.com/" +str(url)
            yield scrapy.Request(url=url, callback=self.parse)



    def parse_show(self,response):
        item =BossItem()
        item["name"] = response.css('.info-primary .name h1::text').get()
        item["salary"] =response.css('.name .salary::text').get().replace("\n","").strip()
        item["ed"] = ".".join(response.css('.job-banner .info-primary p ::text').getall())
        item["company_name"] = response.css('.job-sec .name::text').get()
        item["address"] = response.css('.location-address ::text').get()
        item["position"] = ";".join(response.css('.job-sec .text ::text').getall()).strip().replace("\n","")
        item["url"] = response.meta.get("url")
        yield item

