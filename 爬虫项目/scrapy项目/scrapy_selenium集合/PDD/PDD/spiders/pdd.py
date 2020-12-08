# -*- coding: utf-8 -*-
import scrapy
from PDD.items import PddItem

class PddSpider(scrapy.Spider):
    name = 'pdd'
    allowed_domains = ['mobile.yangkeduo.com']
    start_urls = ['http://mobile.yangkeduo.com/']

    def start_requests(self):
        url = "https://mobile.yangkeduo.com/mall_page.html?mall_id=1274420&msn=rviqsucl6t4qo7cgehvf5eo5y4_axbuy&goods_id=58070244799&refer_page_name=login&refer_page_id=10169_1578198357118_nnUZXFsZHe&refer_page_sn=10169&mall_tab_key=mall_goods&page_id=10039_1586842468847_9w6ftwdvom&sort_type=1&is_back=1"
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = PddItem()
        lis = response.css("._3w8gnMK_")
        for li in lis:
            item["name"] = li.css("._30RB5FtA span::text").get()
            item["price"] = (li.css("._1yPO5MOK  ._2ehdLmxB ::text").get()).strip("已拼").strip("件")
            if item["price"].endswith("万"):
                item["price"] = (item["price"].strip("万"))*10000

            item["count"] = li.css("._1yPO5MOK  ._1Wn5uaO1 ::text").get()
            item["image_url"] = li.css("._16dSD4Rc img ::attr('src')").get()

            yield item