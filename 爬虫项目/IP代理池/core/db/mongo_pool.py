"""
实现代理池的数据模块
作用：用于对proxies集合进行数据库的相关操作
目标：实现对数据库增删改查相关操作
步骤：
1，在init中，建立数据连接，获取要操作的集合，在del方法中关闭数据库连接
2,提供基础的增删该查功能
   1，实现插入功能
   2，实现修改功能
   3，实现删除代理：根据代理IP删除代理
   4，查询所有代理IP的功能
3.提供代理API模块使用的功能
  1，实现查询功能：根据条件进行查询，可以指定查询数量，先分数降序，速度升序保证优质的代理IP在上面
  2，实现根据协议类型 和 要访问网站的域名，获取代理IP列表
  3，实现根据协议类型 和 要访问网站的域名，随机获取代理IP列表
  4，实现把指定域名添加到指定IP的disable_domain列表中
"""
import pymongo,random
from pymongo import MongoClient
from settings import MONGO_URL
from utils.log import logger
from domain import Proxy
class MongoPool(object):
    def __init__(self):
        #在init中，建立数据连接，获取要操作的集合
        self.client=MongoClient(MONGO_URL)
        #获取要操作的集合
        self.proxies=self.client.proxies_pool.proxies

    # 在del方法中关闭数据库连接
    def __del__(self):
        self.client.close()

    # 1，实现插入功能
    def insert_one(self,proxy):
        count=self.proxies.count_documents({'_id':proxy.ip})
        if count ==0:
            #我们使用proxy.ip作为，MongoDB中数据的主键：_id
            dic=proxy.__dict__
            dic['_id']=proxy.ip
            self.proxies.insert_one(dic)
            logger.info('插入新的代理：{}'.format(proxy))
        else:
            logger.warning("已存在的代理：{}".format(proxy))

    # 2，实现修改功能
    def update_one(self,proxy):
        self.proxies.update_one({'_id':proxy.ip},{'$set':proxy.__dict__})
    # 3，实现删除代理：根据代理IP删除代理
    def delete_one(self,proxy):
        self.proxies.delete_one({'_id':proxy.ip})
        logger.info("删除代理IP：{}".format(proxy))

    # 4，查询所有代理IP的功能
    def find_all(self):
        cusor=self.proxies.find()
        for item in cusor:
            # yield item
            #删除_id 这个key
            item.pop('_id')
            proxy=Proxy(**item)
            yield proxy

    def find(self,conditions={},count=0):
        """
        实现查询功能：根据条件进行查询，可以指定查询数量，先分数降序，速度升序保证优质的代理IP在上面
        :param conditions: 查询条件字典
        :param count: 限制最多取出多少个代理IP
        :return: 返回满足要求代理IP（proxy对象）列表
        """
        cursor=self.proxies.find(conditions,limit=count).sort([('score',pymongo.DESCENDING),('speed',pymongo.ASCENDING)])
        #准备列表，用于存储查询代理IP
        proxy_list=[]
        # 遍历cursor
        for item in cursor:
            item.pop('_id')
            proxy=Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list
    def get_proxies(self,protocol=None,domain=None,count=0,nick_type=2):
        """
        # 实现根据协议类型和要访问网站的域名，获取代理IP列表
        :param protocal: 协议：http,https
        :param domain: 域名：jd.com
        :param count: 用于限制获取多个IP，默认是限制所有
        :param nick_type: 匿名类型，默认，获取高匿的代理IP
        :return: 满足要求代理IP
        """
        #定义查询条件
        conditions={'nick_type':nick_type}
        #根据协议，指定查询条件
        if protocol is None:
            #如果没有传入协议类型，返回支持http 和https 的代理
            conditions['protocol']=2
        elif protocol.lower()=='http':
            conditions['protocol'] = {'$in':[0,2]}
        else:
            conditions['protocol'] = {'$in': [1,2]}
        if domain:
            conditions['disable_domains']={'$nin':[domain]}
        #返回满足要求代理IP
        return self.find(conditions,count=count)
    def random_proxy(self,protocol=None,domain=None,count=0,nick_type=2):
        """
               # 实现根据协议类型和要访问网站的域名，获取代理IP列表
               :param protocal: 协议：http,https
               :param domain: 域名：jd.com
               :param count: 用于限制获取多个IP，默认是限制所有
               :param nick_type: 匿名类型，默认，获取高匿的代理IP
               :return: 满足要求的随机一个代理IP(Proxy对象)
        """
        proxy_list=self.get_proxies(protocol='protocol',domain=domain,count=count,nick_type=nick_type)
        #从proxy_list中随机选择一个IP返回
        return random.choice(proxy_list)
    def disable_domain(self,ip,domain):
        """
        实现把指定域名添加到指定IP的disable_domain列表中
        :param ip: IP地址
        :param domain: 域名
        :return: 如果返回True,就表示添加成功了，返回False添加失败了
        """
        #如果disable_domains 字段中没有这个区域名，才添加
        if self.proxies.count({'_id':ip,'disable_domains':domain})==0:
           self.proxies.update_one({'_id':ip},{'$push':{'disable_domains':domain}})
           return True
        return False

if __name__ == '__main__':
    mongo = MongoPool()
    # print(mongo.random_proxy(protocol=2,domain=None,count=1,nick_type=2))
    # proxy = Proxy('39.137.69.7', port='80')
    # mongo.insert_one(proxy)#插入
    # proxy = Proxy('117.80.86.239',port='8060',speed=20)
    # mongo.update_one(proxy)#修改
    # mongo.delete_one(proxy)#删除
    # for proxy in mongo.find_all():
    #     print(proxy)# 查询所有ip
    # dic={ "ip" : "117.80.86.221", "port" : "8060", "protocol" : 0, "nick_type" :0, "speed" : 8.2, "area" : None, "score" : 50, "disable_domains" : [ "jd.com"]}
    # dic = {"ip": "117.80.86.983", "port": "8080", "protocol": 1, "nick_type": 0, "speed": 2.2, "area": None,
    #        "score": 50, "disable_domains": ["taobao.com"]}
    # dic = {"ip": "117.80.86.876", "port": "8060", "protocol": 2, "nick_type": 0, "speed": 1, "area": None,
    #        "score": 50, "disable_domains": ["jd.com"]}
    # dic = {"ip": "117.80.87.295", "port": "8060", "protocol": 2, "nick_type": 0, "speed": 2, "area": None,
    #        "score": 45, "disable_domains": []}
    # dic = {"ip": "117.80.87.999", "port": "8060", "protocol": 1, "nick_type": 0, "speed": 2.9, "area": None,
    #        "score": 48, "disable_domains": ["taobao.com"]}
    # proxy=Proxy(**dic)
    # mongo.insert_one(proxy)
    for proxy in mongo.find():
    # for proxy in mongo.find({'protocol':0},count=2):#count 获取几条数据
        print(proxy)
    # for proxy in mongo.get_proxies(protocol='https',domain='taobao.com'):#domain 过滤掉的网站
    #     print(proxy)
    # mongo.disable_domain('117.80.87.999','baidu.com')