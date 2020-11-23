import asyncio,aiohttp,requests,time
from lxml import etree
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}
async def get_request(url): #封装成协程对象
    print("正在请求",url)
    # page_text = requests.get(url,headers=headers)   requests是一个不支持异步模块的代码
    async with aiohttp.ClientSession() as sess:  #实例化一个请求对象
         async with await sess.get(url=url,headers=headers) as response:
             page_text = await response.text()
             # print(page_text)
             return page_text

def parse(t): #解析函数的封装
    # print("参数",t)
    page_text = t.result() #解析函数获取请求页面源码
    print(page_text)
    # tree =etree.HTML(page_text)
    # print(tree)

urls =[
    "https://www.baidu.com",
    "https://www.hao123.com",
    "https://www.jd.com"
]

if __name__ == '__main__':
    tasks =[] #多任务列表
    #创建协程对象
    for url in urls:
        c = get_request(url) # 这是一个协程对象
        task = asyncio.ensure_future(c) #任务对象  对协程对象的进一步封装
        task.add_done_callback(parse)  # 给task 绑定一个回调函数  任务执行结束后执行回调函数
        tasks.append(task)
    #创建事件循环对象
    loop =asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks)) #必须使用wait方法对task进行封装才可