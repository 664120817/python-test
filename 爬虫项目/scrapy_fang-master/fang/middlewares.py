# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import base64
# 代理服务器
proxyServer = "https://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H19Z0E6404E0L4ED"
proxyPass = "BC7E524A1BD445E2"

# for Python2
# proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)

# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        print(proxyServer,"ip")
        print (proxyAuth)
        request.headers["Proxy-Authorization"] = proxyAuth
        request.meta['dont_redirect'] = True #请求不成功，不跳转到其他页面，再次重新请求


class UserAgentDownloadMiddleware (object):
    USER_AGENT = [
        'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)'
    ]

    def process_request(self,request,spider):
        user_agent = random.choice(self.USER_AGENT)
        request.headers['User-Agent'] = user_agent


from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By  #WebDeriverWait 负责循环等待的
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC #expected_conditions类  负责条件
from scrapy.http import HtmlResponse
from logging import getLogger

class SeleniumMiddleware():
    print("开始")
    def __init__(self):
        self.browser = webdriver.PhantomJS()
    def process_request(self, request, spider):
        print("123456")
        url = request.url
        wait = WebDriverWait(self.browser, 10)
        self.browser.get(url)
        try:

            self.browser.get(url)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
             return HtmlResponse(url=request.url, status=500, request=request)
