import threading,time
#自定义线程类
class MyThread(threading.Thread):

    def __init__(self,num):
        #调用父类的init方法
        super().__init__()
        self.num = num
    #重写父类的run方法
    def run(self):
        for i in range(5):
            print("正在执行子线程的run方法",i,self.name,self.num)
            time.sleep(0.5)


if __name__ == '__main__':
    #创建对象
    mythread = MyThread(100)
    mythread.start()