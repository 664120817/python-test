#启动服务端 ：scrapyd     登陆：127.0.0.1:6800      参考：https://www.jianshu.com/p/ddd28f8b47fb

#客服端部署项目  在scrapy项目目录下，有一个scrapy.cfg的配置文件：
'''[settings]
default = china.settings

[deploy:demo] # 名称 可以任意取名
url = http://localhost:6800/ # http://服务端IP地址:6800
project = china''' #对应的项目名称

#scrapy.cfg的配置文件同一目录  开启命令行 执行scrapyd-deploy        出现  Unknown target: default   执行成功

#执行   scrapyd-deploy demo（所取名称） -p china（项目名）          上传完成

#启动爬虫 ： curl http://localhost:6800/schedule.json -d project=china（项目名） -d spider=china(spiders文件下的爬虫名)

#取消爬虫 ： curl http://127.0.0.1:6800/cancel.json -d project=（项目名） -d job=启动爬虫生成的ID（33ac5f860bc111eb8c13309c23fd35bf）

#代码实现
import requests
#启动爬虫
'''
url = 'http://localhost:6800/schedule.json'
data={
    'project':项目名,
    'spider': 爬虫名
}
resp = requests.post(url,data =data)
'''
#停止爬虫
'''
url = 'http://localhost:6800/cancle.json'
data={
    'project':项目名,
    'spider': 爬虫名
}
resp = requests.post(url,data =data)
'''