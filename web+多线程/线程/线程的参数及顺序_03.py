import time
import threading
#定义函数
def sing(a,b,c):
    for i in range(5):
        print("唱歌",a,b,c)
        time.sleep(0.5)
def dance():
    for i in range(5):
        print("跳舞")
        time.sleep(0.5)


if __name__ == '__main__':
    #3种方法传递参数
    # #元组传递  threading.Thread(target="函数名",args=(参数1，参数2,......))
    # thread_sing=threading.Thread(target=sing, args=(10,100,1000))

    # # 字典传递  threading.Thread(target="函数名",kwargs=("参数名"：参数值，......))
    # thread_sing=threading.Thread(target=sing, kwargs={"a":10,"b": 100,"c": 1000})

    #混合字典和元组传递  threading.Thread(target="函数名",kwargs=("参数名"：参数值，......)，args=(参数1，参数2,......))
    thread_sing = threading.Thread(target=sing,args=(99,), kwargs={ "c": 100, "b": 1000})
    # 创建线程对象
    thread_dance = threading.Thread(target=dance)
    # 启动子线程
    thread_sing.start()
    thread_dance.start()