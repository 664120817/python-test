import time
def index():
    #处理请求 index.py 请求
    return "This is index show"

def center():
   # 处理请求 index.py 请求
   return "This is center show"

def gettime():
    # 处理请求 index.py 请求
    return "This is gettime show {}".format(time.ctime())