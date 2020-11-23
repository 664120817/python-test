import time,asyncio

async def get_request(url): #封装成协程对象
    print("正在请求",url)
    time.sleep(2)
    print("请求结束",url)
    return "返回的数"

def task_callback(t): #回调函数的封装
    print("参数",t)
    print(t.result())

if __name__ == '__main__':
    c = get_request("www.baidu.com") # 这是一个协程对象
    task = asyncio.ensure_future(c) #任务对象  对协程对象的进一步封装
    task.add_done_callback(task_callback)# 给task 绑定一个回调函数  任务执行结束后执行回调函数
    #创建事件循环对象
    loop =asyncio.get_event_loop()
    loop.run_until_complete(task) #将任务对象注册到事件循环中且开启事件循环