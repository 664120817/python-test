import scrapy,requests

from fang.spiders.ajk import SfwSpider
import base64
import re
import time
from io import BytesIO
from fontTools.ttLib import TTFont
from lxml import etree
from redis import StrictRedis
import pickle

def add_category_to_redis():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }
    start_urls = 'https://gz.zu.anjuke.com'
    redis = StrictRedis(host="localhost", port=6379, db=0, password=None)
    response=requests.get(start_urls,headers=headers)
    response=etree.HTML(response.text)
    region_url_list = response.xpath("//div[contains(@class,item)]/span/div/a//@href")
    region_url_list = region_url_list[1:-2]  # 取得想要的区域link链接
    for region_url in region_url_list:
        print("region_url=%s"%region_url)
        url = region_url + "p1/"
        data = pickle.dumps(url)
        # 添加到商品爬虫redis_key指定的list
        redis.lpush(SfwSpider.redis_key, data)

if __name__ == "__main__":
    add_category_to_redis()