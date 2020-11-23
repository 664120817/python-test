#打猴子补丁  打补丁： 在不修改程序源码的情况下，为程序添加原来不支持的功能
from gevent import monkey
monkey.patch_all() #破解所有

import time,gevent
#创建生成器1
def work1():
    while True:
        print("正在执行work1",gevent.getcurrent()) #没有产生新的线程 在原线程自动划分不同编号
        time.sleep(0.5) #默认情况 不被gevent 识别为耗时操作 需要打补丁
        # gevent.sleep(0.5)
        #打补丁： 在不修改程序源码的情况下，为程序添加原来不支持的功能

#创建生成器1
def work2():
    while True:
        print("正在执行work2",gevent.getcurrent())
        # time.sleep(0.5)
        gevent.sleep(0.5)

if __name__ == '__main__':
    #创建greenlet的对象
    g1=gevent.spawn(work1)
    g2=gevent.spawn(work2)
    g1.join() #让主线程等待协程执行完毕后再退出
    # gevent.joinall() 批量让携程join