# from gevent import monkey
# monkey.patch_all()
from gevent.pool import Pool


from selenium import webdriver
import requests
import time
from redis import StrictRedis, ConnectionPool
import pickle,random

class GenGsxtCookie():
    def __init__(self):
        #链接redis
        self.redis = StrictRedis(host="localhost", port=6379, db=1, password=None)
        # self.redis.delete('bkzf_cookies')#清空redis_cookies数据库
        self.chromeOptions = webdriver.ChromeOptions()
        # #创建携程池对象
        # self.pool=Pool()
    def get_porpy(self):
       try:
           response=requests.get('http://localhost:16888/random?protocol=http')
           if response.status_code == 200:
               ip=response.text
               print(ip)
               ips ={
               # "http":"http://117.191.11.110：8080",
               "http":ip
               }
               # response = requests.get(url="http://httpbin.org/ip", proxies=ips)
               response = requests.get(url="https://wh.zu.ke.com/zufang", proxies=ips)
               print(response.text)
               if response.status_code == 200 :
                  return ip
               else:
                    self.get_porpy()
       except Exception:
           self.get_porpy()


    def cookies_dict(self,i):
            ip=self.get_porpy()
            print(ip,'i:',i)
            proxies={
                                 '--proxy-server':str(ip)
                                 }
            print("proxies:",proxies)
            user_agent ='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            # 设置代理
            self.chromeOptions.add_argument('--proxy-server='+str(ip))
            self.chromeOptions.add_argument('user-agent={}'.format(user_agent))
            print("chromeOptions:",self.chromeOptions)
            # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
            browser = webdriver.Chrome(chrome_options = self.chromeOptions)
            # 查看本机ip，查看代理是否起作用
            browser.get("https://wh.zu.ke.com/zufang")
            # print(browser.page_source)
            cookies = browser.get_cookies()
            # cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]
            # # join()连接字符串数组。将字符串、元组、列表中的元素以指定的字符(分隔符)连接生成一个新的字符串
            # cookies = ';'.join(item for item in cookie)

            # 把代理IP ，User - Agent，Cookie放到字典中，序列化后，存储到Redis的list中
            if cookies and ip :
                cookies_dict = {
                    'cookies': cookies,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                    'proxy': ip,
                }
                print('cookies_dict',cookies_dict)
                # 链接redis
                # 序列化后，存储到Redis的list中
                self.redis.lpush('bkzf_cookies', pickle.dumps(cookies_dict))

                # 退出，清除浏览器缓存
                browser.quit()
                # browser.close()

    def run(self):
        #3,实现一个run方法，用于开启多个异步来执行这个方法
        for i in range(50):
            self.cookies_dict(i)
        #     self.pool.apply_async(self.cookies_dict,args=str(i))
            time.sleep(1)
        # #让主线程等待所以携程任务完成
        # self.pool.join()

if __name__ ==  '__main__':
    ggc = GenGsxtCookie()
    ggc.run()


    #取值
    redis = StrictRedis(host="localhost", port=6379, db=1, password=None)

    #从Redis 中随机取出Cookie来使用，关闭页面重定向。
    count=redis.llen('bkzf_cookies')#获取redis随机长度
    random_index=random.randint(0,count-1)#随机获取redis的索引值
    print(random_index)
    cookie_data=redis.lindex('bkzf_cookies',random_index) #根据随机索引值取出redis数据
    #反序列化，把redis 二进制转换为字典
    cookie_dict=pickle.loads(cookie_data)
    print(cookie_dict)

    # {'cookies': {'__jsl_clearance': '1591201775.761|0|fJz39jBSjOCftFfUgNpnW1quQZc%3D',
    #              '__jsluid_h': 'fb28bf1f4c3921ea6c32dd2df94eb72b'},
    #  'user_agent': 'Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17',
    #  'proxy': 'http://103.138.226.115:3128'}