from multiprocessing import Process
import time

def work(name):
    print(name,"进程执行了")
    time.sleep(5)

if __name__ == '__main__':
   #创建进程对象：
    
    p1=Process(target=work,args=("p1",))
    p2=Process(target=work,args=("p2",))
    p3=Process(target=work,args=("p3",))
    p1.start()
    p2.start()
    p3.start()
