from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By  #WebDeriverWait 负责循环等待的
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC #expected_conditions类  负责条件
from scrapy.http import HtmlResponse

class SeleniumMiddleware(object):
    print("开始")
    def __init__(self):
        self.browser = webdriver.Ie()
    def process_request(self, request, spider):
        print("123456")
        url = request.url
        print(url)
        wait = WebDriverWait(self.browser, 10)
        self.browser.get(url)
        # html = self.browser.page_source
        # print(html)
        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
