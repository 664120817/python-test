"""
新建项目
gerapy init 生成gerapy数据包，进入gerapy文件夹
gerapy migrate 数据库初始化，生成SQLite数据库保存主机配置信息和部署版本等，
gerapy runserver 启动这台机器的8000端口 开启gerapy服务，浏览器链接 http://127.0.0.1:8000/
账号：（root,478ha）

"""
#部署项目  在scrapy项目目录下，有一个scrapy.cfg的配置文件：
'''[settings]
default = china.settings

[deploy:demo] # 名称 可以任意取名
url = http://localhost:6800/ # http://服务端IP地址:6800
project = china''' #对应的项目名称   将配置好的项目拉进 gerapy 一 projects 中jian'toufuhao

#启动scrapyd 服务器：  scrapyd