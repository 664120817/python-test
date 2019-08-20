"""
实现代理池的API模块
目标：
步骤：
    实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
    实现根据协议类型和域名，提供获取多个高可用代理IP的服务
    实现给指定的IP上追加不可用域名的服务
实现：
 1，在proxy_api.py中，创建ProxyApi类
 2，实现初始方法
    1，初始一个Flask的web服务
    2，实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
       可用通过 protocol 和 domain 参数对ip进行过滤
       protocol:当前请求的协议类型
       domain :当前请求域名
    3，实现根据协议类型和域名，提供获取多个高可用代理IP的服务
       可用通过 protocol 和 domain 参数对ip进行过滤
       实现给指定的IP上追加不可用域名的服务
    4，如果在获取ip的时候，有指定域名参数，将不再获取IP，从而进一步提高代理IP的可用性
 3，实现run方法，用于启动Flask的web服务
 4，实现start的类方法，用于通过类名，启动服务
"""
import json
from flask import Flask,request
from core.db.mongo_pool import MongoPool
from settings import PROXIES_MAX_COUNT
class ProxyApi():
    def __init__(self):
        #初始一个Flask的web服务
        self.app=Flask(__name__)
        #创建MongoPool对象，用于操作数据库
        self.mongo_pool=MongoPool()
        @self.app.route('/random')
        def random():
            """
            # 实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
            # 可用通过protocol和domain 参数对ip进行过滤
            # protocol: 当前请求的协议类型
            # domain: 当前请求域名
            :return:
            """
            protocol=request.args.get('protocol')
            domain=request.args.get('domain')
            print(protocol)
            print(domain)
            proxy=self.mongo_pool.random_proxy(protocol,domain,count=PROXIES_MAX_COUNT)
            if protocol:
                return '{}://{}:{}'.format(protocol,proxy.ip,proxy.port)
            else:
                return  '{}:{}'.format(proxy.ip,proxy.port)
        @self.app.route('/proxies')
        def proxies():
            # 实现根据协议类型和域名，提供获取多个高可用代理IP的服务
            # 可用通过protocol和domain参数对ip进行过滤
            # 实现给指定的IP上追加不可用域名的服务
            #获取协议：http/https
            protocol=request.args.get('proxies')
            #区域名：jd.com
            domain=request.args.get('domain')
            proxies=self.mongo_pool.get_proxies(protocol,domain,count=PROXIES_MAX_COUNT)
            #proxies 是一个 Proxy对象的列表，但是Proxy对象不能进行josn序列化，需要转化字典列表
            proxies=[proxy.__dict__ for proxy in proxies]
            #返回json格式值串
            return json.dumps(proxies)

        @self.app.route('/disable_domain')
        def disable_domain():
            # 如果在获取ip的时候，有指定域名参数，将不再获取IP，从而进一步提高代理IP的可用性
            ip=request.args.get('ip')
            domain=request.args.get('domain')
            if ip is None:
                return "请提供ip参数"
            if domain is None:
                return '请提供域名domain参数'
            self.mongo_pool.disable_domain(ip,domain)
            return "{} 禁用域名 {} 成功".format(ip,domain)

    # 实现run方法，用于启动Flask的web服务
    def run(self):
        self.app.run('0.0.0.0',port=16888)

    # 实现start的类方法，用于通过类名，启动服务
    @classmethod
    def start(cls):
        proxy_api = ProxyApi()
        proxy_api.run()
if __name__ == '__main__':
    ProxyApi.start()