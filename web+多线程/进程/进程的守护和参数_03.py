from multiprocessing import Process
import time

def work(a,b,c):
    for i in range(5):
        print(a,b,c,"进程执行了")
        time.sleep(5)

if __name__ == '__main__':
    # 创建进程对象：
    # 3种方法传递参数
    # #元组传递  Process(target="函数名",args=(参数1，参数2,......))
    # thread_work=Process(target=work, args=(10,100,1000))

    # # 字典传递  Process(target="函数名",kwargs=("参数名"：参数值，......))
    # thread_work=Process(target=work, kwargs={"a":10,"b": 100,"c": 1000})

    # 混合字典和元组传递  Process(target="函数名",kwargs=("参数名"：参数值，......)，args=(参数1，参数2,......))
    thread_work = Process(target=work, args=(99,), kwargs={"c": 100, "b": 1000})
    #子进程守护主进程
    thread_work.daemon =True
    thread_work.start()

    #终止子进程运行
    thread_work.terminate()