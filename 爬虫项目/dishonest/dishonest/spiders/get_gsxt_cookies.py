"""
实现生成cookie 的脚本

1，创建gen_gsxt_cookies.py文件，在其中创建GenGsxtCookie的类
2，实现一个方法，用于把一套代理IP，User-Agent,Cookie绑定在一起的信息放到Redis的list中
    随机获取一个User-Agent
    随机获取一个代理IP
    获取request的session对象
    把User-Agent，通过请求头，设置给session对象
    把代理IP，通过proxies，设置给session对象
    使用session对象，发送请求，获取需要的cookie信息
    把代理IP ，User-Agent，Cookie放到字典中，序列化后，存储到Redis的list中
3，实现一个run方法，用于开启多个异步来执行这个方法。
注：为了和下载器中间件交互方便，需要再settings.py中配置一些常量

"""
#打猴子补丁 一定要在requestszhiq打
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool


import random,requests,re,js2py,pickle

from redis import StrictRedis,ConnectionPool
from dishonest.settings import USER_AGENTS,COOKIES_KEY,COOKIES_PROXY_KEY,COOKIES_USER_AGENT_KEY,REDIS_COOKIES_KEY
class GenGsxtCookie():
    def __init__(self):
        #链接redis
        self.redis = StrictRedis(host="localhost", port=6379, db=0, password=None)
        self.redis.delete('redis_cookies')#清空redis_cookies数据库
        #创建携程池对象
        self.pool=Pool()
    def push_cookie_to_redis(self):
        while True:
            try:
                # 实现一个方法，用于把一套代理IP，User - Agent, Cookie绑定在一起的信息放到Redis的list中
                # 随机获取一个User - Agent
                user_agent=random.choice(USER_AGENTS)
                # 随机获取一个代理IP
                response = requests.get('http://localhost:16888/random?protocol=http')
                proxy=response.content.decode()
                # 获取request的session对象
                session=requests.session()
                # 把User - Agent，通过请求头，设置给session对象
                session.headers={ 'User-Agent': user_agent }
                # 把代理IP，通过proxies，设置给session对象
                session.proxies={'http':proxy}
                # 使用session对象，发送请求，获取需要的cookie信息
                index_url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
                response = session.get(index_url)
                # print(response.status_code)
                # print(response.content.decode())
                # 1,提取script 标签中的js
                js = re.findall(r'<script>(.*?)</script>', response.content.decode())[0]
                # print(js)
                # 2，由于这种加密JS，最终指向的js代码，都是在eval函数中的，所以'{eval'(替换为){code=(， 然后就可以通过code,获取真正要执行的js了
                js = js.replace('{eval(', '{code=(')
                # 3,需要执行JS
                # 3.1,获取执行js的环境
                context = js2py.EvalJs()
                context.execute(js)
                # 3.2 打印code的值
                print(context.code)
                # 3.3获取生成Cookie的js
                cookies_code = re.findall(r"document.(cookie=.*?)\+';Expires", context.code)[0]
                # print(cookies_code)
                # 在js2py中，是不能使用 'document','window'这些浏览器中对象
                # var _1a=document.createElement('div');_1a.innerHTML='<a href=\\'/\\'>_21</a>';_1a=_1a.firstChild.href
                # js2py是无法处理的，需要能看懂上诉js代码
                # var _34=document.createElement('div');_34.innerHTML='<a href=\'/\'>_15</a>';_34=_34.firstChild.href
                # _34='http://www.gsxt.gov.cn'
                # cookies_code=re.sub(r"var\s+(\w+)=document.createElement\('\w+'\);\w+.innerHTML='<a href=\\'/\\'>\w+</a>';\w+=\w+.firstChild.href",r"var /1='http://www.gsxt.gov.cn'",cookies_code)
                cookies_code = re.sub(r"var\s+(\w+)=document.+?firstChild.href", r"var \1='http://www.gsxt.gov.cn'",
                                      cookies_code)
                # print(cookies_code)
                # 执行js，生成我们需要的cookie信息
                context.execute(cookies_code)
                # 打印cookie
                # print(context.cookie)
                # 上面用session.headers=headers添加headers，下面就不用传递headers
                cookies = context.cookie.split('=')
                # session.cookies.update({cookies[0]:cookies[1]})
                session.cookies.set(cookies[0], cookies[1])  # 将JS的cokies 设置添加进去
                session.get(index_url)  # 发送请求
                # print(session.cookies)
                # 获取cookie字典
                cookies = requests.utils.dict_from_cookiejar(session.cookies)
                print(cookies)
                # 把代理IP ，User - Agent，Cookie放到字典中，序列化后，存储到Redis的list中
                cookies_dict={
                     COOKIES_KEY:cookies,
                     COOKIES_USER_AGENT_KEY:user_agent,
                     COOKIES_PROXY_KEY:proxy,
                 }
                print(cookies_dict)
                #序列化后，存储到Redis的list中
                self.redis.lpush(REDIS_COOKIES_KEY,pickle.dumps(cookies_dict))
                break
            except Exception as ec:
                print(ec)

    # 实现一个run方法，用于开启多个异步来执行这个方法
    def run(self):
        #3,实现一个run方法，用于开启多个异步来执行这个方法
        for i in range(100):
            self.pool.apply_async(self.push_cookie_to_redis)
        #让主线程等待所以携程任务完成
        self.pool.join()


if __name__ ==  '__main__':
    ggc=GenGsxtCookie()
    ggc.run()