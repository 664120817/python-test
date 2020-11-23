import time,os
import multiprocessing
"""#创建一个函数，用于模拟文件拷贝
def copy_work():
    print("正在拷贝文件....",multiprocessing.current_process().pid)
    time.sleep(0.5)

if __name__ == '__main__':
    #创建进程池，长度为3
    pool =multiprocessing.Pool(3)
    for i in range (10):
        #进程池同步方式拷贝文件 pool.apply（函数名,(传递函数参数1，参数2.....))
        # pool.apply(copy_work)
        #异步拷贝文件方式  需要做2点
        # pool.close() 表示不再接收新的任务
        # pool.join() 让主进程等待进程池 执行接收后再退出
        pool.apply_async(copy_work)
    pool.close()
    pool.join()"""

#创建一个函数，用于模拟文件拷贝
def copy_work(source_dir,dest_dir,file_name):
    #拼接源文件和目标文件路径
    source_path = source_dir +"/" +file_name
    dest_path =dest_dir +"/" +file_name
    #读取文件写入到文件
    with open(source_path,"rb") as source_file:
        #创建目标文件
        with open(dest_path,"wb")as dest_file:
            while True:
                data=source_file.read(1024)
                if data:
                    dest_file.write(data)
                else:
                    break

    print("正在拷贝文件....",multiprocessing.current_process().pid)
    time.sleep(0.5)

if __name__ == '__main__':
    #定义变量 保存文件夹 目标文件夹
    source_dir ="/home/hao/Pictures/image"
    dest_dir = "/home/hao/Desktop/1"
    # 再目标路径创建新的文件夹
    try:
        os.mkdir(dest_dir)
    except Exception as e :
        print("文件已经存在")
    #获取源文件的所有文件名
    file_list =os.listdir(source_dir)

    #创建进程池，长度为3
    pool =multiprocessing.Pool(3)
    #遍历所有文件名
    for file_name in file_list :
        #进程池同步方式拷贝文件 pool.apply（函数名,(传递函数参数1，参数2.....))
        # pool.apply(copy_work)
        #异步拷贝文件方式  需要做2点
        # pool.close() 表示不再接收新的任务
        # pool.join() 让主进程等待进程池 执行接收后再退出
        pool.apply_async(copy_work,(source_dir,dest_dir,file_name))
    pool.close()
    pool.join()