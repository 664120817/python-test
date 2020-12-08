# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import ZFHourseItem
from fang.reflection import region_reflection
from datetime import datetime
class SfwSpider(scrapy.Spider):
    name = 'sfw'

    allowed_domains = ['fang.com']
    start_urls = ['https://gz.zu.fang.com/']
    base_url = 'https://gz.zu.fang.com/'

    def parse(self, response):
        url_list = response.xpath("//div[contains(@class,search-listbox)]/dl[@id='rentid_D04_01']/dd[1]/a/@href").getall()
        url_list = url_list[1:-2]
        print(url_list)
        for url in url_list:
            url = self.base_url +url
            yield scrapy.Request(url=url, callback=self.parse_region,meta={'url':url})


    def parse_region(self,response):
        url=response.meta.get('url')
        base_url = 'https://gz.zu.fang.com'
        dls = response.xpath('//*[@id="listBox"]/div[2]/dl[contains(@class,list)]//dd/p[@class="title"]/a/@href')
        dl_cont = dls.getall()
        for index, dl in enumerate(dl_cont):
            # print(index,dl_cont[index])
            complete_url = base_url + dl_cont[index]
            print('complete_url',complete_url)

            yield scrapy.Request(url=complete_url, callback=self.parse_detail)
        pages = response.css('.fanye .txt::text').extract_first()
        pages = int(re.findall(r'.*?(\d+).*?', pages)[0])
        for new_page in range(2, pages + 1):
            cmp_url = url+"i3{}/".format(new_page)
            print(cmp_url)
            yield scrapy.Request(url=cmp_url, callback=self.parse_region)


    def parse_detail(self,response):
        cont = response.css( '.tab-cont-right')
        address =cont.css('.tr-line .link-under ::text').extract()
        # print(cont)
        cityid = '440100'
        cityname = '广州'
        try:
            commname = address[0]
            distname = address[1]+"区"   # 白云
            distid = address[1]
        except:
            commname=None
        try:
            distid = region_reflection[distid]
        except:
            distid =None
        # print(commname, distname, distid)
        publishtime = (response.xpath("//div//p//span/text()").extract()[1] ).split(' ')[1]
        publishtime = datetime.strptime(publishtime,'%Y-%m-%d')
        # print(publishtime)
        rentarea = response.css('.w132 .tt::text').extract_first()
        # print(rentarea)
        rentarea =re.findall(r'.*?(\d+).*?',rentarea)[0]
        # print(rentarea)
        rentarea = float(rentarea)
        # print(rentarea)
        roomcnt = response.css('.w182 .tt::text').extract_first()
        roomcnt = roomcnt.split("室")[0]
        roomcnt = int(roomcnt)
        # print(roomcnt)
        totalprice = response.css('.sty1 i::text').extract_first()
        totalprice = float(totalprice)
        try:
            unitprice  = float(totalprice)/float(roomcnt)
        except:
            unitprice =None
        rent_way  = response.css('.w146 .tt::text').extract_first()
        # 过滤条件： 广州周边小区，六室房、合租房，满足其中任意一个条件就过滤掉
        if distname not in region_reflection or roomcnt >= 6 or rent_way == '合租' or unitprice == None:

           print("不符合返回条件，%s,%s,%s,%s"%(distname,roomcnt,rent_way,unitprice))
        else:
            print("item已经返回")
            item = ZFHourseItem(id='null', cityid=cityid,  distid=distid,
                                publishtime=publishtime, rentarea=rentarea, roomcnt=roomcnt, totalprice=totalprice,
                                unitprice=unitprice, commname=commname
                                )
            print(item,'xxxxx')
            yield item





