# -*- coding: utf-8 -*-
import scrapy
from jianshu.items import JianshuItem

class JsSpider(scrapy.Spider):
    name = 'js'
    allowed_domains = ['www.jianshu_selenium.com']
    start_urls = ['http://www.jianshu_selenium.com/']

    def parse(self, response):
        # print(response.text)
        lis=response.css(".note-list .title::attr(href)").getall()
        for li in lis :
           url = "https://www.jianshu_selenium.com"+li
           print(url)

           yield scrapy.Request(url=url, callback=self.parse_text )
           # break



    def parse_text(self,response):
       # print(response.text)
       item = JianshuItem()
       item['title'] = response.css("._gp-ck ._1RuRku::text").get()
       item['user_url'] = "https://www.jianshu_selenium.com"+response.css("._gp-ck ._1OhGeD::attr(href)").get()
       item['date'] = response.css("._gp-ck .s-dsoj time::text").get()
       item['dz']  = response.css("._gp-ck .s-dsoj span:last-child::text").get()
       item['text'] = "  ".join(response.css("._gp-ck ._2rhmJa p::text").getall())
       yield item
       # print(item)


