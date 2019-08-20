from settings import MAX_SCORE

class Proxy(object):
    def __init__(self,ip,port,protocol=-1,nick_type=-1,speed=-1,area=None,score=MAX_SCORE,disable_domains=[]):
        self.ip=ip  # ip: 代理的ip地址
        self.port=port # port: 代理的IP端口号
        self.protocol=protocol # portocol: 代理IP支持的协议类型，http是0，https是1，https和http都支持是2
        self.nick_type=nick_type  #nick_type: 代理的匿名程度，高匿：0，匿名：1，透明：2
        self.speed=speed # speed: 代理IP的响应速度，S
        self.area=area  # area: 代理IP所在地区
        self.score=score   # score: 代理IP的评分，用于衡量代理的可用性；默认分值可以通过配置文件进行配置。在进行代理可用性检
        # 查的时候，没遇到一次请求失败就减1分，减到0的时候从池中删除，如果检查代理可以用，恢复默认分值
        self.disable_domains=disable_domains # disable_domains: 不可用域名列表，有些代理IP在某种域名下不可用，但是在其他域名下可用



    # 提供__str__方法，返回数据字符串
    def __str__(self):
        return str(self.__dict__)

"""
1.定义代理IP的数据模型类
目标：定义代理IP的数据模型类
步骤：
定义proxy类，继承object
实现__init__方法，负责初始化，包含如下字段：
ip:代理的ip地址
port:代理的IP端口号
portocol:代理IP支持的协议类型，http是0，https是1，https和http 都支持是2
nick_type:代理的匿名程度，高匿：0，匿名：1，透明：2
speed:代理IP的响应速度，S
area:代理IP所在地区
score:代理IP的评分，用于衡量代理的可用性；默认分值可以通过配置文件进行配置。在进行代理可用性检查的时候，没遇到一次请求失败就减1
分，减到0的时候从池中删除，如果检查代理可以用，恢复默认分值
disable_domains:不可用域名列表，有些代理IP在某种域名下不可用，但是在其他域名下可用
在配置文件：settings.py中 定义MAX_SCORE=50，表示代理IP的默认最高分数
提供__str__方法，返回数据字符串
"""