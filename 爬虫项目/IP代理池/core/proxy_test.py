"""
9.实现代理池的检验模块
目的：检查代理IP可用性，保证代理池中代理IP基本可用
思路：
1，在proxy_test.py中，创建ProxyTest类
2，提供一个run方法，用于处理检测代理IP核心逻辑
3，从数据库中获取所有代理IP
4，遍历IP列表
5，检查代理可用性
6，如果代理不可用，让代理分数减一，如果代理分数等于0则从数据库中删除该代理
7，如果代理可用，就恢复该代理的分数，更新到数据库中

为了提高检查的速度，使用异步来执行检查任务
0，在init方法中 创建队列和协程池
1，把检测的代理IP，放到队列中
2，把检查一个代理可用性的代码，抽取到一个方法中；从队列中获取代理IP，进行检查；检查完毕
3，通过异步回调，使用死循环不断执行这个方法
4，开启多个一个异步任务，来处理代理IP的检测；可以通过配置文件指定异步数量
"""
#打猴子补丁
from gevent import monkey
monkey.patch_all()
#导入协程池
from gevent.pool import Pool
import schedule,time
from queue import Queue
from core.db.mongo_pool import MongoPool
from settings import MAX_SCORE,TEST_PROXIES_ASYNC_COUNT,TEST_PROXIES_INTERVAL
from core.proxy_vaildate.httpbin_validator import check_proxy
class ProxyTester():
    def __init__(self):
        #创建操作数据库的MonggoPool对象
        self.mongo_pool=MongoPool()
        # 在init方法中创建队列和协程池
        self.queue=Queue()
        self.coroutine_pool = Pool()
    #提供一个run方法，用于处理检测代理IP核心逻辑
    def __check_callback(self,temp):
        self.coroutine_pool.apply_async(self.__check_one_proxy,callback=self.__check_callback)
    def run (self):
        # 从数据库中获取所有代理IP
        proxies=self.mongo_pool.find_all()
        # 遍历IP列表
        for proxy in proxies:
            #把要检测的代理IP,放到队列中
            self.queue.put(proxy)
        # 开启多个一个异步任务，来处理代理IP的检测；可以通过配置文件指定异步数量
        for i in  range(TEST_PROXIES_ASYNC_COUNT):

            #通过异步回调，使用死循环不断执行这个方法，
            self.coroutine_pool.apply_async(self.__check_one_proxy,callback=self.__check_callback)
            #让当前线程，等待队列任务完成
        self.queue.join()
    def __check_one_proxy(self):
        #检查一个代理IP的可用性
        #把检查一个代理可用性的代码，抽取到一个方法中；
        # 从队列中获取代理IP，进行检查；检查完毕
        proxy=self.queue.get()
        # 检查代理IP可用性
        proxy = check_proxy(proxy)
        # 如果代理不可用，让代理分数减一，如果代理分数等于0则从数据库中删除该代理
        if proxy.speed == -1:
            proxy.score -= 1
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                self.mongo_pool.update_one(proxy)  # 否则更新该ip
        else:
            proxy.score = MAX_SCORE  # 如果代理可用，就恢复该代理的分数，更新到数据库中
            self.mongo_pool.update_one(proxy)
        #调度队列的task_done方法
        self.queue.task_done()

    @classmethod
    def start(cls):
        # 1，定义一个start的类方法
        # 2，创建当前类的对象，调用run方法
        rs = ProxyTester()
        rs.run()
        # 3，使用schedule模块，每隔一定时间，执行当前对象的run方法
        # 修改配置文件，增加爬虫运行时间间隔的配置，单位为小时
        schedule.every(TEST_PROXIES_INTERVAL).hours.do(rs.run)
        while True:
            schedule.run_pending()
            time.sleep(2)


if __name__ =='__main__':
   ProxyTester.start()