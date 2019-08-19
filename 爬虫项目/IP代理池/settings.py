#在配置文件：settings.py中 定义MAX_SCORE=50，表示代理IP的默认最高分数
MAX_SCORE=50
#日志配置信息
import logging
#默认配置
LOG_LEVEL=logging.DEBUG#默认等级
LOG_FMT="%(asctime)s---%(lineno)s----%(name)s: %(message)s"#默认打印格式
LOG_DATEFMT="%Y-%m-%d %H:%M:%S"#默认时间格式
LOG_FILENAME="log.log" #默认日志文件名称

#测试代理IP的超时时间
TEST_TIMEOUT=10

#MONGODB数据库的URL
MONGO_URL='mongodb://localhost:27017/'

#爬虫全类名，路径：模块.类名
PROXIES_SPIDERS=[
'我爱自学.IP代理池.core.proxy_spider.proxy_spiders.XiciSpider',
'我爱自学.IP代理池.core.proxy_spider.proxy_spiders.IP3366Spider',
'我爱自学.IP代理池.core.proxy_spider.proxy_spiders.KDLSpider',
'我爱自学.IP代理池.core.proxy_spider.proxy_spiders.PLLSpider',
# '我爱自学.IP代理池.core.proxy_spider.proxy_spiders.Ip66Spider',
]

# 修改配置文件，增加爬虫运行时间间隔的配置，单位为小时
RUN_SPIDERS_INTERVAL=24

#配置检测代理IP的异步数量
TEST_PROXIES_ASYNC_COUNT=20

# 检查代理IP的时间间隔，单位为小时
TEST_PROXIES_INTERVAL=2

#配置获取的代理IP最大数量；这个越小可用性就越高；但是随机性越差
PROXIES_MAX_COUNT = 50
