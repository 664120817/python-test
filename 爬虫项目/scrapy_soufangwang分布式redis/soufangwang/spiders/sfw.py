# -*- coding: utf-8 -*-
import scrapy
import re
from soufangwang.items import NewfangwangItem,ErsfangwangItem
#所有城市URL链接
url='https://www.fang.com/SoufunFamily.htm'

#武汉城市链接
url='https://wuhan.fang.com/'
#武汉新房链接
url='https://wuhan.newhouse.fang.com/house/s/'
#武汉二手房
url='https://wuhan.esf.fang.com/'

#北京是个例外
#北京新房 url='https://newhouse.fang.com/house/s/'
#北京二手房url='https://esf.fang.com/'

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
       trs=response.xpath('//div[@class="outCont"]//tr')
       poryince=None
       for tr in trs:
           tds=tr.xpath('.//td[not(@class)]')
           poryince_td=tds[0]
           poryince_text=poryince_td.xpath(".//text()").get()
           poryince_text=re.sub(r"\s","",poryince_text)
           if poryince_text:
               poryince=poryince_text
           #不爬取海外城市
           if poryince == "其它":
               continue

           city_td= tds[1]
           city_links=city_td.xpath('.//a')
           for city_link in city_links:
               print(city_link.css('a ::text').extract()),"666"
               if city_link.css('a::text').extract()[0] == "武汉":
                   city=city_link.xpath('.//text()').get()
                   city_url=city_link.xpath(".//@href").get()
                   # print(poryince,city,city_url)
                   #构建新房的URL链接
                   url_module=city_url.split("//")
                   schemo=url_module[0]
                   domain=url_module[1]
                   print(domain)
                   if "bj." in domain:
                       newhouse_url='https://newhouse.fang.com/house/s/b91/'
                       esfhouse_url ='https://esf.fang.com/house/i31/'
                   else:
                       newhouse_url=schemo+"//"+"newhouse."+domain+"house/s/b91/"#新房链接
                       esfhouse_url=schemo+"//"+"esf."+domain +"house/i31/"#二手房链接
                   print(poryince,city,newhouse_url,esfhouse_url)
                   yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"info":(poryince,city)})
                   yield scrapy.Request(url=esfhouse_url,callback=self.parse_esfhouse,meta={"info":(poryince,city)})
               #     break
               # break
    def parse_newhouse(self,response):
        poryince,city=response.meta.get("info")
        lis=response.xpath('//div[contains(@class,"nl_con")]/ul/li')
        num = 1
        for li in lis:
                name=li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
                if name is not None:
                    name=name.strip()
                if name==None:
                    continue
                else:
                    house_type_list=li.xpath('.//div[contains(@class,"house_type")]//text()').getall()
                    house_type_list=list(map(lambda x:re.sub(r'"\s"',"",x),house_type_list))
                    rooms=",".join(list(filter(lambda x:x.endswith("居"),house_type_list))) #匹配以居字结尾的
                    area="".join(li.xpath('.//div[contains(@class,"house_type")]/text()').getall())
                    area=re.sub('\s|－|/',"",area)
                    address=li.xpath('.//div[@class="address"]/a/@title').get()
                    district_text="".join(li.xpath('.//div[@class="address"]//a//text()').getall())
                    try:
                        district=re.findall(r'.*\[(.*?)\].*',district_text)[0]
                    except Exception:
                        district=""
                    sale_text="|".join(li.xpath('.//div[contains(@class,"fangyuan")]//text()').getall())
                    sale=re.sub(r'\s',"",sale_text)
                    price="".join(li.xpath('.//div[@class="nhouse_price"]//text()').getall())
                    if price is not None:
                        price=price.strip()
                    origin=li.xpath('.//div[@class="nlcd_name"]/a/@href').get()
                    if origin is not None:
                        origin_url="https:"+origin

                    item=NewfangwangItem(name=name,rooms=rooms,area=area,address=address,district=district,sale=sale,price=price,origin_url=origin_url,poryince=poryince,city=city)
                    yield item
                    last_url=response.xpath('.//div[@class="page"]//a[@class="active"]/@href').get()
                    if not last_url:
                        num+=1
                        yield scrapy.Request(url=response.urljoin("/house/s/b9"+str(num)+"/"),callback=self.parse_newhouse,meta={"info":(poryince,city)})
            # print(name,rooms,area,address,district,sale,price,origin)

    def parse_esfhouse(self,response):
        print(response.text)
        item = ErsfangwangItem()
        poryince,city = response.meta.get("info")
        dls=response.xpath('//div[contains(@class,"shop_list")]//dl')
        num=1
        for dl in dls:
            name=dl.css('.add_shop a::text').extract_first()
            if name is not None:
                item['name']=name.strip()
            item['price']="".join(dl.css('.price_right span b::text').extract())+"/".join(dl.css('.price_right span::text').extract())
            rooms="".join(dl.css('.tel_shop ::text').extract())
            item['rooms']=re.sub(r"\s","",rooms)
            address="".join(dl.css('.add_shop a ::text').extract())+"----"+"".join(dl.css('.add_shop span::text').extract())
            item['address'] = re.sub(r"\s", "", address)
            origin_url = dl.css('.clearfix a::attr(href)').extract_first()
            item['origin_url'] = response.urljoin(origin_url)
            item['poryince']=poryince
            item['city']=city
            yield item
            last_url=response.css('.page_al span::attr("class")').extract_first()[-1]
            if last_url !="on":
                num+=1
                yield scrapy.Request(url=response.urljoin("/house/i3"+str(num)+"/"),callback=self.parse_esfhouse,meta={"info":(poryince,city)})







