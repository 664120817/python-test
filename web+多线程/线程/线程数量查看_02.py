import time
import threading
#定义函数
def saySorry():
    print("对不起，我错了！",threading.current_thread())
    time.sleep(0.5)

def music():
    for i in range(5):
        print("音乐",threading.current_thread())
        time.sleep(0.5)

def move():
    for i in range(5):
        print("动作",threading.current_thread())
        time.sleep(0.5)



if __name__  == "__main__":
    #线程的名称
    print(threading.current_thread())#当前线程对象
    #获取活跃的线程列表
    thread_list = threading.enumerate()
    thread_num =len(thread_list)
    print("当前活跃线程数量：",thread_num)
    #创建线程对象
    thread_saySorry=threading.Thread(target=saySorry)
    thread_move = threading.Thread(target=move)
    thread_music = threading.Thread(target=music)
    #启动子线程
    thread_saySorry.start()
    thread_move.start()
    thread_music.start()
    # 获取活跃的线程列表
    while True:
        thread_list = threading.enumerate()
        thread_num = len(thread_list)
        print("当前活跃线程数量：", thread_num)
        time.sleep(0.5)
        if thread_num <= 1 :
            break