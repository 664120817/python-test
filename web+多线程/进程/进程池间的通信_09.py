
import multiprocessing,time
#写入数据队列的函数
def write_queue(queue):
    for i in range(5):
        #判断队列是否已满
        if queue.full():
            print("队列已满")
            break
        queue.put(i)
        print("已写入",i,multiprocessing.current_process().pid)
        time.sleep(0.5)
def read_queue(queue):
    while True:
        #判断队列是否为空
        if queue.qsize() == 0:
            print("队列已空")
            break
        #从列表读取数据
        value =queue.get()
        print("已读取",value,multiprocessing.current_process())

if __name__ == '__main__':
    #创建进程池队列
    queue = multiprocessing.Manager().Queue(5)
    # 创建进程池，长度为3
    pool = multiprocessing.Pool(2)
    for i in range(10):
        # 进程池同步方式拷贝文件 pool.apply（函数名,(传递函数参数1，参数2.....))
        # pool.apply(write_queue,(queue,))
        # 异步拷贝文件方式  需要做2点
        # pool.close() 表示不再接收新的任务
        # pool.join() 让主进程等待进程池 执行接收后再退出
        result=pool.apply_async(write_queue,args=(queue,))
        result.wait() #wait() 方法类似join() 表示先让当前进程执行完毕，后续进程才能启动
        pool.apply_async(read_queue,args=(queue,))
    pool.close()
    pool.join()