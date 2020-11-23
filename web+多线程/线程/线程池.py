import time
from multiprocessing.dummy import Pool as ThreadPool  #是线程，之所以dummy（中文意思“假的”）


def num(num):
    for i in range(num):
        print(i)
    time.sleep(3)

if __name__ == "__main__":
    thread=ThreadPool(3) #开启多少个线程
    thread.map(num,[6,8,6]) #num 调用的函数  [6,8,6] 传个每个函数的参数

