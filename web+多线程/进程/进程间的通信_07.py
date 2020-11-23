#1,准备两个进程
#2，准备一个队列  一个进程向队列中写入数据，然后把队列传入另一个进程
# 3，另一个进程读取数据

import multiprocessing,time
#写入数据队列的函数
def write_queue(queue):
    for i in range(5):
        #判断队列是否已满
        if queue.full():
            print("队列已满")
            break
        queue.put(i)
        print("已写入",i,multiprocessing.current_process())
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
    #创建一个空的列表
    queue = multiprocessing.Queue(5)
    #创建2个进程，分别写数据，读数据
    write_p=multiprocessing.Process(target=write_queue, args=(queue,))
    read_p = multiprocessing.Process(target=read_queue, args=(queue,))
    write_p.start()
    #优先让数据写入
    write_p.join()
    read_p.start()