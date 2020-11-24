# -*- coding: utf-8 -*-
import scrapy,re,time

from city_house.items import BeikezufangItem
class BkzfSpider(scrapy.Spider):
    name = 'bkzf'
    allowed_domains = ['www.wh.zu.ke.com']
    start_urls = ['https://wh.zu.ke.com/zufang']
    def parse(self, response):
       # print(response.text)
       areas = response.xpath('//*[@id="filter"]/ul[@data-target="area"]/li')
       for area in areas:
           area_name =area.xpath('./a/text()').get()
           area_url = "https://wh.zu.ke.com" + area.xpath('./a/@href').get()
           if area_name != "不限":
               yield scrapy.Request(url=area_url,callback=self.parse_zf,meta={"area_name":area_name},dont_filter=True)
               print(area_name,area_url)
               # break


    def parse_zf(self,response):
        # print(response.text)
        item = BeikezufangItem()
        area_name =response.meta.get("area_name")
        contents =response.css('#content .content__list .content__list--item .content__list--item--main')
        for content in contents:
            try:
                item["city"] = "武汉"
                item["region"] = area_name
                item["url"] = "https://m.ke.com" + content.css('.content__list--item--title a::attr(href)').extract_first()
                house_name= content.css('.content__list--item--title a::text').extract_first()
                item["house_name"]=re.findall(r'\s*(.*?)\s',house_name)[0]
                room = "".join(content.css('.content__list--item--des ::text').extract())
                room= re.sub(r'(\s*)','',room)
                item["house_from"] = room
                item["room"] =re.findall(r'.*/(\d+㎡).*',room)[0]

                item["price"] = content.css('.content__list--item-price em::text').extract_first().strip()
                # print(item)
            except Exception:
                print("解析出错了")

            yield item
            # print(content)

        pages =response.css('.content__pg ::attr(data-url)').get()
        count = re.findall(r"data-totalPage=(\d+) data-curPage", response.text)[0]
        num = re.findall(r"data-curPage=(\d+)>",response.text)[0]
        page = "https://wh.zu.ke.com" + re.sub('{page}',str(int(num)+1),pages)
        print(count, num, page, )
        time.sleep(1)
        if int(num) < int(count) :
           yield scrapy.Request(url=page,callback=self.parse_zf,meta={"area_name":area_name},dont_filter=True)

