# -*- coding: utf-8 -*-

# Scrapy settings for mall_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'mall_spider'

SPIDER_MODULES = ['mall_spider.spiders']
NEWSPIDER_MODULE = 'mall_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mall_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'mall_spider.middlewares.MallSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'mall_spider.middlewares.RandomUserAgent': 200,
   'mall_spider.middlewares.ProxyMiddleware': 201,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'mall_spider.pipelines.MallSpiderPipeline': 300,
   'mall_spider.pipelines.MongDBSpiderPipeline': 299,
   'mall_spider.pipelines.ProuctPipeline': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#配置MongoDB的URL
MONGOBD_URL='mongodb://localhost:27017'
#实现scrapy_reids:在settings 文件中配置scrapy_redis
#REDIS数据连接
REDIS_URL='redis://localhost:6379/0'#redis://[password]@localhost:6379/0  0指定哪个库db=0
#调度器：用于把待爬请求存储到基于Redis的队列
SCHEDULER="scrapy_redis.scheduler.Scheduler"

#去重容器类：用于把已爬指纹存储到基于Redis的set集合中
DUPEFILTER_CLASS="scrapy_redis.dupefilter.RFPDupeFilter"
#是不进行调度持久化：
#如果是true,当程序结束的时候，会保留Redis中已爬指纹和待爬的请求
#如果是false,当程序结束的时候，会清空Redis中已爬指纹和待爬的请求
SCHEDULER_PERSIST=True

# #设置redis为item pipeline
# ITEM_PIPELINES = {
#    'scrapy_redis.pipelines.RedisPipeline': 300,
# }
# #在redis中保持scrapy_redis用到的队列，不会清除redis中的队列，从而可以实现停止和恢复的功能
# SCHEDULER_PERSIST=True
# #设置连接redis的信息
# REDIS_HOST='192.168.2.101' #服务器IP地址
# REDIS_PORT=6379