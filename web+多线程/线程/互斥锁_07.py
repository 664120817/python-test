import threading,time

#定义全局变量  多个线程同时执行，会出现抢资源问题
g_num =100

def work():
    global g_num
    for i in range(1000000):
        lock.acquire()#上锁
        g_num+=1
        lock.release() #解锁
    print("work---------",g_num)

def work2():
    global g_num
    for i in range(1000000):
        lock.acquire()  # 上锁
        g_num += 1
        lock.release()  # 解锁
    print("work2---------", g_num)


if __name__ == "__main__":
    #创建一把互斥锁
    lock=threading.Lock()

    t1=threading.Thread(target=work)
    t2 = threading.Thread(target=work2)
    t1.start()
    t2.start()
    #子线程运行完后打印g_num
    while len(threading.enumerate())!=1:
        time.sleep(1)
    print(g_num)