# -*- coding: utf-8 -*-
import scrapy,json
from ..items import  Category

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['dc.3.cn']
    start_urls = ['https://dc.3.cn/category/get']

    def parse(self, response):
       result=json.loads(response.body.decode("gbk"))
       datas=result['data']
       #遍历数据列表
       item=Category()
       for data in datas:
           #大分类
           b_category=data['s'][0]
           b_category_info=b_category['n']
           item['b_category_name'], item['b_category_url']= self.get_categor_name_url(b_category_info)
           # print("大分类数据{}".format(b_category_info))
           #中分类信息列表
           m_category_s = b_category['s']
           #遍历中分类列表
           for m_category in m_category_s:
               #中分类信息
               m_category_info=m_category['n']
               item['m_category_name'], item['m_category_url'] = self.get_categor_name_url(m_category_info)
               # print("中分类数据{}".format(m_category_info))
               #小分类信息列表
               s_category_s=m_category['s']
               for s_category in s_category_s:
                   s_category_info = s_category['n']
                   item['s_category_name'], item['s_category_url'] = self.get_categor_name_url(s_category_info)
                   # print("小分类数据{}".format(s_category_info))
                   yield item
    def get_categor_name_url(self,category_info):
        """
        根据分类信息，提取名称和URL
        :param category_info:分类信息
        :return:分类的名称和URL
        分类数据格式（三类数据格式）
        1，list.jd.com/list.html?cat=737,794,798|电视||0
          https://list.jd.com/list.html?cat=737,794,798|%E7%94%B5%E8%A7%86||0
        2，6196-6219|水具酒具||0
          https://channel.jd.com/6196-6219.html
        3，737-794-12392|冷柜/冰吧||0
          https://list.jd.com/list.html?cat=737,794,12392
        """
        categorys=category_info.split('|')
        category_url=categorys[0]#分类URL
        category_name=categorys[1]#分类名称
        # URL补全
        if category_url.count('jd.com')==1:# 处理第一类分类URL
            category_url='https://'+category_url
        elif category_url.count('-')==1:# 处理第二类分类URL
            category_url ='https://channel.jd.com/{}.html'.format(category_url)
        elif category_url.count('-')==2:# 处理第二类分类URL
            category_url = category_url.replace('-',',')
            category_url = 'https://list.jd.com/list.html?cat={}'.format(category_url)
        #返回类别名称和URL
        return category_name,category_url
