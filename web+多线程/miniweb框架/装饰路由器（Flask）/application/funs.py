import time

from application import urls
# 装饰器
def route(path):
    def function_out(func):
        urls.route_dict[path] = func
        def function_in():
            func()
        return function_in
    return function_out



@route("/index.py")
def index():
    #处理请求 index.py 请求
    return "This is index show"
@route("/center.py")
def center():
   # 处理请求 index.py 请求
   return "This is center show"
@route("/gettime.py")
def gettime():
    # 处理请求 index.py 请求
    return "This is gettime show {}".format(time.ctime())