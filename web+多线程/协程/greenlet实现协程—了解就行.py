import time
from greenlet import greenlet
#创建生成器1
def work1():
    while True:
        print("正在执行work1")
        time.sleep(0.5)
        g2.switch() #切换g2任务

#创建生成器1
def work2():
    while True:
        print("正在执行work2")
        time.sleep(0.5)
        g1.switch()#切换g1任务


if __name__ == '__main__':
    #创建greenlet的对象
    g1=greenlet(work1)
    g2=greenlet(work2)
    g1.switch()#启动g1任务