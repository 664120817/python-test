"""
1,实现西刺代理爬虫：http://www.xicidaili.com/nn/1
定义一个类，继承通用爬虫类（BasicSpider）
提供urls,group_xpath 和 detail_xpath
"""
from core.proxy_spider.base_spider import BaseSpider
import time,random,requests,re
from utils.http import get_request_headers
class XiciSpider(BaseSpider):
    #准备URL列表
    urls = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1,10)]
    # group_xpath: 分组XPATH，获取包含代理信息标签列表的XPATH
    group_xpath='//*[@id="ip_list"]/tr[position()>1]'#[position()>1]第一个过滤掉
    # detail_xpath: 组内XPATH，获取代理IP详情的信息XPATH，
    detail_xpath={
        'ip':'./td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/text()',
    }
"""
1,实现ip3666代理爬虫：http://www.ip3366.net/free/?stype=1&page=1
定义一个类，继承通用爬虫类（BasicSpider）
提供urls,group_xpath 和 detail_xpath
"""
class IP3366Spider(BaseSpider):
    #准备URL列表
    urls = ['http://www.ip3366.net/free/?stype={}&page={}'.format(i,j) for i in range(1,3) for j in range(1,8)]
    # group_xpath: 分组XPATH，获取包含代理信息标签列表的XPATH
    group_xpath='//*[@id="list"]/table/tbody/tr'
    # detail_xpath: 组内XPATH，获取代理IP详情的信息XPATH，
    detail_xpath={
        'ip':'./td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }
# 实现快代理爬虫：https://www.kuaidaili.com/free/inha/1/
# 定义一个类，继承通用爬虫类（BasicSpider）
# 提供urls, group_xpath和detail_xpath
class KDLSpider(BaseSpider):
    #准备URL列表
    urls = ['https://www.kuaidaili.com/free/{}/{}/'.format(j,i) for j in ["inha","intr"]  for i in range(1,8)]
    # group_xpath: 分组XPATH，获取包含代理信息标签列表的XPATH
    group_xpath='//*[@id="list"]/table/tbody/tr'
    # detail_xpath: 组内XPATH，获取代理IP详情的信息XPATH，
    detail_xpath={
        'ip':'./td[@data-title="IP"]/text()',
        'port': './td[@data-title="PORT"]/text()',
        'area': './td[@data-title="位置"]/text()',
    }
    #当我们两个页面访问时间间隔太短了，就会报错；这是一种反爬手段。
    def get_page_from_url(self,url):
        #随机等待1-3秒
         time.sleep(random.uniform(1,3))
         #调用父类方法，发送请求，获取相应数据
         return super().get_page_from_url(url)
# 实现proxylistplus代理爬虫：https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
# 定义一个类，继承通用爬虫类（BasicSpider）
# 提供urls, group_xpath和detail_xpath
class PLLSpider(BaseSpider):
    #准备URL列表
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1,7)]
    # group_xpath: 分组XPATH，获取包含代理信息标签列表的XPATH
    group_xpath='//*[@id="page"]/table[2]/tr[position()>2]'
    # detail_xpath: 组内XPATH，获取代理IP详情的信息XPATH，
    detail_xpath={
        'ip':'./td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[5]/text()',
    }

# 实现快代理爬虫：http://www.66ip.cn/1.html
# 定义一个类，继承通用爬虫类（BasicSpider）
# 提供urls, group_xpath和detail_xpath
class IP66Spider(BaseSpider):
    #准备URL列表
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1,7)]
    # group_xpath: 分组XPATH，获取包含代理信息标签列表的XPATH
    group_xpath='//*[@id="main"]/div/div[1]/table/tbody/tr[position()>1]'
    # detail_xpath: 组内XPATH，获取代理IP详情的信息XPATH，
    detail_xpath={
        'ip':'./td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }
    #从写方法解决反爬问题
    def get_page_from_url(self, url):
        headers=get_request_headers()
        response=requests.get(url,headers=headers)
        if response.status_code ==521:
           #生成cookies信息，在携带cookies请求
           url = 'http://www.66ip.cn/1.html'
           # url='https://m.guazi.com/wh/dazhong/'
           headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Cookie': '__jsl_clearance=1565788094.68|0|EmOnBjtTOFID8%2BQNO3SBgFgs66A%3D',
               # 'Host':'www.66ip.cn'

           }
           response = requests.get(url, headers=headers)

           return response.content.decode('GBK')
        else:
           return response.content.decode('GBK')

if __name__=="__main__":
    pass
    # spider = XiciSpider()
    # spider =IP3366Spider()
    # spider =KDLSpider()
    # spider=PLLSpider()
    # for proxy in spider.get_proxies():
    #     print(proxy)
#测试：http://www.66ip.cn/1.html
url='http://www.66ip.cn/1.html'
# url='https://m.guazi.com/wh/dazhong/'
headers={
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
  # 'Cookie': '__jsluid_h=387469b6811bed6f8ee5c0c007044f66; __jsl_clearance=1565757516.115|0|aWejWfxOlxd%2BalkWAfq5Ga1aEF8%3D',
  # 'Host':'www.66ip.cn'
  'Cookie':'__jsl_clearance=1565788094.68|0|EmOnBjtTOFID8%2BQNO3SBgFgs66A%3D'
}
response=requests.get(url,headers=headers)
text=response.text
print(response.status_code)
print(response.content.decode('GBK'))
#生成 _ydclearance cookie信息
#1.确定 _ydclearance 是从哪里来的；
#观察发现：这个cookie信息不使用通过服务器响应设置过来的；那么他就是通过JS生成
#2,第一次发送请求的页面中，有一个生成这个cookie的js；执行这段js；生成我们需要的cookie
#这段js是经过加密处理后的js,真正在'po'中。
#提取'jp(107)'调用函数的方法，以及函数
# re.findall(r'',)