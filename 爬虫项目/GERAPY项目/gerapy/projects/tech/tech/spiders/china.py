# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'.*\/index.*\.html')),

        Rule(LinkExtractor(restrict_xpaths='//div[@id = "rank-defList"]//h3'), callback='parse_item',follow=False)
    )


    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
        Title = response.css('#chan_newsTitle::text').get()
        print(Title)
