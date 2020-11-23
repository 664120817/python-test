import time
import threading
#定义函数
def saySorry():
    print("对不起，我错了！")
    time.sleep(0.5)

def music():
    for i in range(5):
        print("音乐")
        time.sleep(0.5)

def move():
    for i in range(5):
        print("动作")
        time.sleep(0.5)



if __name__  == "__main__":
        #创建线程对象
        thread_saySorry=threading.Thread(target=saySorry)
        thread_move = threading.Thread(target=move)
        thread_music = threading.Thread(target=music)
        #启动子线程
        thread_saySorry.start()
        thread_move.start()
        thread_music.start()

