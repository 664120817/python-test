from multiprocessing import Process
import time,multiprocessing,os

def work():
    for i in range(5):
        print("子进程执行了 编号为：",multiprocessing.current_process().pid)
        print("os模块获取子进程编号：", os.getpid(),"获取父进程ID:",os.getppid())
        time.sleep(5)

if __name__ == '__main__':
    #获取主进程名称
    print(multiprocessing.current_process())
    #获取主进程编号：
    print("主进程编号：",multiprocessing.current_process().pid)
    #使用OS模块获取编号
    print("os模块获取主进程编号：",os.getpid())
    #创建进程对象：
    p1=Process(target=work)
    p1.start()
    print("主进程编号：", multiprocessing.current_process().pid)
#杀掉进程 命令行输入
# kill -9 "进程编号"