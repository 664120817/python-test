# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from zhihuuser.items import ZhihuItem
import json
from scrapy_redis.spiders import RedisSpider
class ZhihuSpider(RedisSpider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['http://www.zhihu.com/']
    url_token='excited-vczh'
    redis_key = 'zhihuSpider:start_url'#名字随意
    # url = 'https://www.zhihu.com/people/excited-vczh/activities'
    follws_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    follws_qure='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    def start_requests(self):

        # yield Request(self.url,callback=self.parse_sure)
        yield Request(url=self.follws_url.format(user=self.url_token,include=self.follws_qure,offset=0,limit=20), callback=self.parse_follws)

    def parse_sure(self, response):
        # result=json.loads(response.text)
        print(response)


    def parse_follws(self, response):
      results=json.loads(response.text)
      if 'data' in results.keys():
          for result in results.get("data"):
              item = ZhihuItem()
              item['id']=result.get('id')
              item['name']=result.get('name')
              if ['name']== "[已重置]":
                  continue
              item['url']=result.get('url')
              item['url_token']=result.get('url_token')
              yield item
              yield Request(url=self.follws_url.format(user=result.get('url_token'),include=self.follws_qure,offset=0,limit=20), callback=self.parse_follws)

      if "paging" in results.keys() and results.get('paging').get('is_end') == "false":
          next_page=results.get('paging').get('next')
          yield Request(next_page,callback=self.parse_follws)




