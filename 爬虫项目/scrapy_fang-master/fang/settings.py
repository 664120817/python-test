# -*- coding: utf-8 -*-

# Scrapy settings for fang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fang'

SPIDER_MODULES = ['fang.spiders']
NEWSPIDER_MODULE = 'fang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fang (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
REDIRECT_ENALBED = False
# HTTPERROR_ALLOWED_CODES = [404]
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {

":authority": "gz.zu.anjuke.com",
":method": "GET",
":path": "/fangyuan/haizhu/p3/",
":scheme": "https",
"accept":" text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"accept-encoding":" gzip, deflate, br",
"accept-language":" zh-CN,zh;q=0.9",
"cookie":" ctid=12; aQQ_ajkguid=AA068857-8F17-2A51-6605-3A44D85F25CF; wmda_uuid=6d25751f024495d5474673de81feccd8; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; lps=https%3A%2F%2Fgz.zu.anjuke.com%2Ffangyuan%2Fliwan%2F%7C; wmda_session_id_6289197098934=1568792662449-7912a468-9142-7bea; xzfzqtoken=6Im5fZRAkgm6Eb8DTMLoElBG2TI4v6UjtSilO6c8YW2L5P%2BTPKniZc08em%2BO5a0yin35brBb%2F%2FeSODvMgkQULA%3D%3D",
"referer":" https://gz.zu.anjuke.com/fangyuan/haizhu/",
"upgrade-insecure-requests":" 1",

}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'fang.middlewares.FangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
'fang.middlewares.UserAgentDownloadMiddleware': 543,
'fang.middlewares.ProxyMiddleware':512,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'fang.pipelines.FtxPipeline': 300,
    'fang.pipelines.FangJsonPipeline': 300,

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
#（（ ））

#REDIS数据连接
REDIS_URL='redis://localhost/0'#redis://[password]@localhost:6379/0  0指定哪个库db=0
#调度器：用于把待爬请求存储到基于Redis的队列
SCHEDULER="scrapy_redis.scheduler.Scheduler"

#去重容器类：用于把已爬指纹存储到基于Redis的set集合中
DUPEFILTER_CLASS="scrapy_redis.dupefilter.RFPDupeFilter"
#是不进行调度持久化：
#如果是true,当程序结束的时候，会保留Redis中已爬指纹和待爬的请求
#如果是false,当程序结束的时候，会清空Redis中已爬指纹和待爬的请求
SCHEDULER_PERSIST=False