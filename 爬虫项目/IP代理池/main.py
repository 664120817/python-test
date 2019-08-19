"""
开启三个进程，分别用于启动爬虫，检查代理IP，WEB服务
步骤：
  1，定义一个run方法用于启动代理池
  2，定义一个列表，用于存储要启动的进程
  3，创建启动爬虫的进程，添加到列表
  4，创建启动检测的进程，添加到列表中
  5，创建启动提供API服务的进程，添加到列表中
  6，遍历进程列表，启动所有进程
  7，遍历进程列表，让主进程等待进程的完成
  8，在 if __name__ == '__main__': 中调用run方法

"""
from multiprocessing import Process
from 我爱自学.IP代理池.core.proxy_spider.run_spiders import RunSpider
from 我爱自学.IP代理池.core.proxy_test import ProxyTester
from 我爱自学.IP代理池.core.proxy_api import ProxyApi
def run():
    # 2，定义一个列表，用于存储要启动的进程
    process_list=[]
    # 3，创建启动爬虫的进程，添加到列表
    process_list.append(Process(target=RunSpider.start))
    # 4，创建启动检测的进程，添加到列表中
    process_list.append(Process(target=ProxyTester.start))
    # 5，创建启动提供API服务的进程，添加到列表中
    process_list.append(Process(target=ProxyApi.start))
    # 6，遍历进程列表，启动所有进程
    for process in process_list:
        process.daemon=True #设置守护进程
        process.start()
    # 7，遍历进程列表，让主进程等待进程的完成
    for process in process_list:
        process.join()
if __name__ =='__main__':
    run()