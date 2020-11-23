import threading,time

def work():
    for i in range(10):
        print("正在工作..........")
        time.sleep(0.5)

if __name__ == "__main__":
    thread_work= threading.Thread(target=work)
    #线程守护：子线程守护主线程
    thread_work.setDaemon(True) #如果主线程结束 子线程也结束
    thread_work.start()

    time.sleep(2)
    print("Game Over")
    #让程序退出，主线程结束
    exit()