# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html



"""
9.1 实现随机User-Agent的中间件
步骤
1，准备user-agent列表
在middlewares.py中，实现RandomUserAgent类
实现process_request方法，设置随机请求头
"""

# 准备user-agent列表

import random,requests,pickle
from dishonest.spiders.gsxt import GsxtSpider
from dishonest.settings import USER_AGENTS
class RandomUserAgent(object):
    # 实现process_request方法，设置随机请求头
    # 如果是公示系统爬虫，就直接跳过
    def process_request(self, request, spider):
        if isinstance(spider,GsxtSpider):
            return None
        else:
            request.headers['user-agent'] = random.choice(USER_AGENTS)
        return None
"""
实现代理IP中间件
1，在middlewares.py中，实现ProxyMiddleware类
2, 实现process_request方法
"""
class ProxyMiddleware(object):

    # 实现process_request方法
    def process_request(self, request, spider):
        #如果是公示系统爬虫，就直接跳过
        if isinstance(spider,GsxtSpider):
            return None
        else:
            # 1，获取协议头
            protocol = request.url.split('://')[0]
            # 2，构建代理IP请求的URL，发送请求，获取代理IP
            proxy_url = 'http://localhost:16888/random?protocol={}'.format(protocol)
            response = requests.get(proxy_url)
            # 2，把代理IP设置给request.meta['proxy]
            request.meta['proxy'] = response.content.decode()
        return None

"""
实现公式系统中间类
步骤
   1.实现process_request方法，从Redis中随机取出cookies来使用，关闭页面重定向。
   2，实现process_response方法，如果相应码不是200 或 没有内容重试
"""

from redis import StrictRedis
from dishonest.settings import USER_AGENTS,COOKIES_KEY,COOKIES_PROXY_KEY,COOKIES_USER_AGENT_KEY,REDIS_COOKIES_KEY
class GsxtCookieMiddleware(object):
    def __init__(self):
        #链接redis
        self.redis = StrictRedis(host="localhost", port=6379, db=0, password=None)
    def process_request(self,request,spider):
        if isinstance(spider, GsxtSpider):
            #从Redis 中随机取出Cookie来使用，关闭页面重定向。
            count=self.redis.llen(REDIS_COOKIES_KEY)#获取redis随机长度
            random_index=random.randint(0,count-1)#随机获取redis的索引值
            print(random_index)
            cookie_data=self.redis.lindex(REDIS_COOKIES_KEY,random_index) #根据随机索引值取出redis数据
            #反序列化，把redis 二进制转换为字典
            cookie_dict=pickle.loads(cookie_data)
            # print(cookie_dict)
            #把cookie信息设置request
            request.headers['user-agent']=cookie_dict[COOKIES_USER_AGENT_KEY]
            #设置请求代理IP
            request.meta['proxy'] = cookie_dict[COOKIES_PROXY_KEY]
            #设置cookie信息
            request.cookies =cookie_dict[COOKIES_KEY]
            #设置不要重定向
            request.meta['dont_redirect'] = True #请求不成功，不跳转到其他页面，再次重新请求
            # print(request.cookies)
        return None

    def process_response(self,request,response,spider):
        #相应码不是200 或 没有内容重试
        # print(response.text)
        if isinstance(spider, GsxtSpider):
            if response.status != 200 or response.body == b'':
                print("请求失败：",response.status)
                req = request.copy() #备份请求
                #设置请求不过滤
                req.dont_filter = True
                #把请求交给引擎
                return req
            print("请求成功：",response.status)
            return response
        return response




# from scrapy import signals
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By  #WebDeriverWait 负责循环等待的
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import  expected_conditions as EC #expected_conditions类  负责条件
# from scrapy.http import HtmlResponse
# from logging import getLogger
# import time
# class SeleniumMiddleware():
#     def __init__(self, timeout=30):
#         self.timeout = timeout
#         self.browser = webdriver.Chrome()
#         # self.browser.set_page_load_timeout(self.timeout)
#         # self.wait = WebDriverWait(self.browser, self.timeout)
#
#     # def __del__(self):
#     #     self.browser.close()
#
#     def process_request(self, request, spider):
#         """
#         用PhantomJS抓取页面
#         :param request: Request对象
#         :param spider: Spider对象
#         :return: HtmlResponse
#         """
#
#         try:
#             self.browser.get(request.url)
#             wait = WebDriverWait(self.browser, self.timeout)
#             time.sleep(5)
#             print(self.browser.get_cookies())
#             # print(self.browser.page_source,"444")
#             return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
#                             status=200)
#         except TimeoutException:
#             return HtmlResponse(url=request.url, status=500, request=request)