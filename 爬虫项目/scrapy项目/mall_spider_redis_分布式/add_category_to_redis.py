"""
在项目文件下创建 add_category_to_redis.py
实现方法 add_category_to_redis
链接MongoDB  ,链接Redis
读取MongoDB中分类信息，序列化后，添加到商品爬虫redis_key指定的list
关闭mongodb
在if __name__ == "__main__": 中调用 add_category_to_redis方法
"""
from pymongo import MongoClient
from redis import StrictRedis
from 我爱自学.爬虫项目.mall_spider_redis_分布式.mall_spider.spiders.jd_product import JdProductSpider
from 我爱自学.爬虫项目.mall_spider_redis_分布式.mall_spider.settings import REDIS_URL,MONGOBD_URL
import pickle
def add_category_to_redis():
    # 链接MongoDB, 链接Redis
    mongo = MongoClient(MONGOBD_URL) # mongo = MongoClient(host='localhost', port=27017)
    redis = StrictRedis.from_url(REDIS_URL)# redis = StrictRedis(host="localhost", port=6379, db=0, password=None)
    # 读取MongoDB中分类信息，序列化后，添加到商品爬虫redis_key指定的list
    collection=mongo.jd.category #collection= mongo['jd']['category']
    # 读取分类信息
    cursor=collection.find()
    for category in cursor:
        #序列化字典数据
        data=pickle.dumps(category)
        #添加到商品爬虫redis_key指定的list
        redis.lpush(JdProductSpider.redis_key,data)
    mongo.close()#关闭MongDB

if __name__ == "__main__":
    add_category_to_redis()