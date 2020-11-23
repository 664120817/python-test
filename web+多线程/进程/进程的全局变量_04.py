import multiprocessing
#定义全局变量  多个线程同时执行，会出现抢资源问题
g_num =100

def work():
    global g_num
    for i in range(1000000):
        g_num+=1
    print("work---------",g_num)

def work2():
    global g_num
    for i in range(100):
        g_num += 1
    print("work2---------", g_num)


if __name__ == "__main__":
    work_p=multiprocessing.Process(target=work)
    work2_p = multiprocessing.Process(target=work2)
    work_p.start()
    work2_p.start()

    #主进程变量
    print("主进程变量---------", g_num)