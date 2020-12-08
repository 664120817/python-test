# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import pickle,random
from redis import StrictRedis
from city_house.settings import COOKIES_KEY,COOKIES_PROXY_KEY,COOKIES_USER_AGENT_KEY,REDIS_COOKIES_KEY
class GsxtCookieMiddleware(object):
    def __init__(self):
        #链接redis
        self.redis = StrictRedis(host="localhost", port=6379, db=1, password=None)
    def process_request(self,request,spider):
        # if isinstance(spider, GsxtSpider):
        #从Redis 中随机取出Cookie来使用，关闭页面重定向。
        count=self.redis.llen(REDIS_COOKIES_KEY)#获取redis随机长度
        random_index=random.randint(0,count-1)#随机获取redis的索引值
        print(random_index)
        cookie_data=self.redis.lindex(REDIS_COOKIES_KEY,random_index) #根据随机索引值取出redis数据
        #反序列化，把redis 二进制转换为字典
        cookie_dict=pickle.loads(cookie_data)
        print(cookie_dict)
        #把cookie信息设置request
        request.headers['user-agent']=cookie_dict[COOKIES_USER_AGENT_KEY]
        #设置请求代理IP
        # request.meta['proxy'] = cookie_dict[COOKIES_PROXY_KEY]
        #设置cookie信息
        request.cookies =cookie_dict[COOKIES_KEY]
        # request.cookies ="lianjia_uuid=abe46d83-81ce-45ce-9401-544ab83ed6a6; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22172795a8ca8500-0b7aaddb54bcc2-3a65420e-2073600-172795a8ca9971%22%2C%22%24device_id%22%3A%22172795a8ca8500-0b7aaddb54bcc2-3a65420e-2073600-172795a8ca9971%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fA1xR00B6KC0nsg607_uPIX000002mUxdC00000r9nZvn.THvkVQOZdI2LEsK85H63njb1nWRkg1f4gv99UdqsusK15yFhnjRYuW7hnj0snH0knWf0IHYsrHPjwWm4fbuan1u7rHN%22%2C%22%24latest_referrer_host%22%3A%22sp0.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%B4%9D%E5%A3%B3%E6%89%BE%E6%88%BF%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wywuhan%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; digv_extends=%7B%22utmTrackId%22%3A%22%22%7D; ke_uuid=ef176815a18c5fdd0e6a3309b6921f6b; _ga=GA1.2.987666540.1591196345; _gid=GA1.2.1034219200.1591196345; select_city=420100; __xsptplus788=788.1.1591196360.1591196430.5%234%7C%7C%7C%7C%7C%23%23paztsk_3m5nfYzKCrEefI4r-Hni8ENql%23; lianjia_ssid=18d99e61-2ae4-49e2-adb8-aa6d8180c700; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZDc5NzkwNTkwMGVlMTYwMWFiYTBmZGE2Yjc3NTNjZDJjZWE0MTE0ZTBmODhhMjQ1NzViNjY4YTZkODEyZDg2YTZmYmY0MDFlN2RhZTZlYzFlOTQ1Y2ZmZGEyZjUxZjkxYjMwNzY3ZTVlNjFjN2M4N2YzY2ZjZGM4NDhhYmU4MWY1OTIxMTZhZDgwODkxYzhhNjU5NTkyMzE3ZWY3NmZlZGJiOTU0NWY4ZjA0NjMxOGFjNjhkMGIxMmEzNjRhZTgzMDRlNzdkM2RlODMyNGMwODQ1OWEwNTk1NGU0ZmIzNTEyOTVmNDU4YzUwNTA5OWJhYWYwMTNlZDVhODIzYTcwMmFkOWY1MzhiMmM0MmIxZGQ1ZGUyMzQ0NjI1OTgyNWFkZWRlM2Q3ZjFiNDk0OWE2NDNjZDY0NzM3NjIxZTkzZGNcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiZDdkZTA5NWNcIn0iLCJyIjoiaHR0cHM6Ly93aC56dS5rZS5jb20venVmYW5nIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0="
        #设置不要重定向
        # request.meta['dont_redirect'] = True #请求不成功，不跳转到其他页面，再次重新请求
        print(cookie_dict[COOKIES_KEY])
        return None

    def process_response(self,request,response,spider):
        #相应码不是200 或 没有内容重试
        # print(response.text)
        # if isinstance(spider, GsxtSpider):
        if response.status != 200 or response.body == b'':
            print("请求失败：",response.status)
            req = request.copy() #备份请求
            #设置请求不过滤
            req.dont_filter = True
            #把请求交给引擎
            return req
        print("请求成功：",response.status)
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
