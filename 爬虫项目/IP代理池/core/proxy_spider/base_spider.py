
"""
1，定义一个BaseSpider类，继承objet
2,提供三个类 成员变量
    urls:代理IP网址的URL的列表
    group_xpath:分组XPATH，获取包含代理信息标签列表的XPATH
    detail_xpath:组内XPATH，获取代理IP详情的信息XPATH，格式为：{'ip':'xx','port':'xx','area':'xx'}
3,提供初始方法，传入爬虫URL列表，分组XPATH，详情（组内）XPATH
4，对外提供一个获取代理IP的方法
   1，遍历URL列表，获取URL
   2，根据发生请求，获取页面数据
   3，解析页面，提取数据，封装为Proxy对象
   返回Proxy 对象列表
"""
import time
import requests
from lxml import etree
from domain import Proxy
from utils.http import get_request_headers

# 定义一个BaseSpider类，继承objet
class  BaseSpider(object):
    # 提供三个类成员变量
    # urls: 代理IP网址的URL的列表
    urls=[]
    # group_xpath: 分组XPATH，获取包含代理信息标签列表的XPATH
    group_xpath=''
    # detail_xpath: 组内XPATH，获取代理IP详情的信息XPATH，格式为
    detail_xpath={}
    # 提供初始方法，传入爬虫URL列表，分组XPATH，详情（组内）XPATH
    def __init__(self,urls=[],group_xpath='',detail_xpath={}):
        if urls:
            self.urls=urls
        if group_xpath:
            self.group_xpath=group_xpath
        if detail_xpath:
            self.detail_xpath=detail_xpath
    def get_page_from_url(self,url):
        #根据URL 发送请求，获取页面数据
        response=requests.get(url,headers=get_request_headers())
        return response.content

    def get_first_from_list(self,lis):
        #如果列表中有元素返回第一个，否则为空
        return lis[0] if len(lis) !=0 else""
    def get_proxies_from_page(self,page):
        #解析提取数据，封装为Proxy对象
        element=etree.HTML(page)
        print(element.text)
        #获取包含代理IP信息的标签列表
        trs=element.xpath(self.group_xpath)
        # print(trs,"666")
        #遍历trs，获取代理IP相关信息
        for tr in trs:
            ip= self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port=self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area=self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy=Proxy(ip,port,area=area)
            yield proxy
    # 对外提供一个获取代理IP的方法
    def get_proxies(self):
        # 1，遍历URL列表，获取URL
          for url in self.urls:
              print(url)
        # 2，根据发生请求，获取页面数据
              page=self.get_page_from_url(url)
        # 3，解析页面，提取数据，封装为Proxy对象
              proxies =self.get_proxies_from_page(page)
              time.sleep(0.3)
        # 4,返回Proxy对象列表
              yield from proxies
if __name__ =="__main__":
    config={
        'urls': ['https://www.kuaidaili.com/free/inha/{}'.format(i) for i in range(1, 4)],
        'group_xpath':'//*[@id="list"]/table/tbody/tr',
        'detail_xpath':{
            'ip':'./td[@data-title="IP"]/text()',
            'port':'./td[@data-title="PORT"]/text()',
            'area': './td[@data-title="位置"]/text()'
        }
    }
    spider=BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)