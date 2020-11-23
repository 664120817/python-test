import multiprocessing
#创建一个长度为3的队列
queue =multiprocessing.Queue(3)
queue.put(1)
queue.put(2)
queue.put(3)

#判断是否已满
isFull =queue.full() #判断队列是否已满，True 满 ， Fasle 未满
print(isFull)

#2取出队列消息的个数
value =queue.get() #取值
print(queue.qsize()) #队列消息的个数

#3判断是否已经为空
isEmpty =queue.empty() #判断队列是否为空，True 空 ， Fasle 不为空
print(isEmpty)


def write_queue(queue):
    print(queue.full())

write_queue(queue)