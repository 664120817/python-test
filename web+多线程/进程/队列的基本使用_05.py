import multiprocessing

#创建队列长度
queue =multiprocessing.Queue(5)#表示能放5个值
queue.put(1)
queue.put("Hello")
queue.put("nice to miss you")
queue.put({"a":10,"c":12})
queue.put("帅哥")
#长度为5，再放入，队列进入阻塞状态，默认队列取出在放入新的值
# queue.put("美女")
#put_nowait() 放值，表示不等待，如果已满，直接报错

#取值
while True:
    value=queue.get()
    print(value)
#当队列已经空的时候，再次get() 程序进入阻塞状态，等待放入新的值，然后再取出
#queue.get_nowait() 当队列已空的时候，不再等待放入新的值，直接报错
