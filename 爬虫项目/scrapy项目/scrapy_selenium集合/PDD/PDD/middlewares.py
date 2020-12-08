# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By  # WebDeriverWait 负责循环等待的
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # expected_conditions类  负责条件
from scrapy.http import HtmlResponse
import time


class PddSpiderMiddleware(object):

    print("开始")
    def __init__(self):
        self.browser = webdriver.Ie()

    def process_request(self, request, spider):
        print("123456")
        url = request.url
        WebDriverWait(self.browser, 10)
        self.browser.get(url)
        # print(self.browser.find_element_by_class_name('_2XuY1YgJ'))
        for i in range(150):
            js = 'window.scrollTo(0,%s)' % (i * 2000)
            self.browser.execute_script(js)
            time.sleep(2)

        # html = self.browser.page_source
        # print(html)
        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)


