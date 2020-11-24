# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By  #WebDeriverWait 负责循环等待的
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC #expected_conditions类  负责条件
from scrapy.http.response.html import HtmlResponse

class SeleniumMiddleware(object):
    def __init__(self, timeout=None):

        self.timeout = timeout
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, self.timeout)

    # def __del__(self):
        # self.browser.close()

    def process_request(self, request, spider):
        try:
            self.browser.get(request.url)
            time.sleep(1)
            if request.url == "http://www.jianshu_selenium.com/" :
                for i in range(20):

                    js = 'window.scrollTo(0,%s)' % (i * 300)
                    self.browser.execute_script(js)
                    time.sleep(0.5)

            # while self.browser.execute_script('alert("To Bottom")'):
            #     self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            #     self.browser.execute_script('alert("To Bottom")')
            #     time.sleep(1)

            try:
                while True:
                    showMore =self.browser.find_element_by_class_name('load-more')
                    showMore.click()
                    time.sleep(1)
                    if not showMore:
                       break
            except Exception:
                pass
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)