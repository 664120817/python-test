"""
实现代理池的校验模块
目标：检查代理IP速度，匿名程度以及支持的协议类型
步骤：
检查代理IP速度和匿名程度；
    代理IP速度：发送请求和获得响应时间间隔
    匿名程度检查：
    1.对 http://httpbin.org/get 或 https://httpbin.org/get 发送请求
    2.如果 响应的headers 中有','分割的两个IP就是透明代理IP
    3.如果 响应的headers 中包含 Proxy-Connection 说明是匿名代理IP
    4.否则就是高匿代理IP
检查代理IP协议类型
如果 http://httpbin.org/get 发送请求成功 说明支持http
如果 https://httpbin.org/get 发送请求成功 说明支持https
"""
import time
import json
import requests
from 我爱自学.IP代理池.utils.http import get_request_headers
from 我爱自学.IP代理池.settings import TEST_TIMEOUT
from 我爱自学.IP代理池.utils.log import logger
from 我爱自学.IP代理池.domain import Proxy
def check_proxy(proxy):
    """
    用于检查指定 代理IP 响应速度，匿名程度，支持协议类型
    :param proxy: 代理IP模型对象
    :return: 检查后的代理IP模型对象
    """
    # 准备代理IP字典
    proxies={
        'http':'http://{}:{}'.format(proxy.ip,proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port)
    }
    #测试该代理IP
    http,http_nick_type,http_speed=__check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies)
    # 代理IP支持的协议类型，http是0，https是1，https和http都支持是2
    if http and https:
        proxy.protocol=2
        proxy.nick_type=http_nick_type
        proxy.speed=http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy

def __check_http_proxies(proxies, is_http=True):
    # 匿名类型 代理的匿名程度，高匿：0，匿名：1，透明：2
    nice_type = -1,#不存在默认-1
    #响应速度，单位S
    speed = -1
    if is_http:
        test_url='http://httpbin.org/get'
    else:
        test_url='https://httpbin.org/get'
    #获取开始时间
    try:
        start=time.time()
        #发送请求，获取响应数据
        # 1.对 http://httpbin.org/get 或 https://httpbin.org/get 发送请求
        response=requests.get(test_url,headers=get_request_headers(),proxies=proxies,timeout=TEST_TIMEOUT)
        print(response.text)
        if response.ok:
            #计算响应速度
            speed= round(time.time()-start,2) #round(,2)代表保留2位小数
            # 匿名程度检查：
            #把响应的JOSN字符串，转化为字典
            dic=json.loads(response.text)
            #获取来源IP：origin
            origin=dic['origin']
            proxy_connection=dic['headers'].get('Proxy-Connection',None)
            # 2.如果 响应的headers 中有','分割的两个IP就是透明代理IP
            if ',' in origin:
                nice_type=2
            # 3.如果 响应的headers 中包含 Proxy-Connection 说明是匿名代理IP
            elif  proxy_connection:
                nice_type = 1
            # 4.否则就是高匿代理IP
            else:
                nice_type = 0
            return True,nice_type,speed
        return False,nice_type,speed
    except Exception as es:
        # logger.exception(es)
        return False,nice_type,speed
if __name__=='__main__':
    proxy=Proxy('117.80.86.239',port='3128')
    print(check_proxy(proxy))
