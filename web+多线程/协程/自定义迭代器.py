class MyList(object):
    #初始化方法
    def __init__(self):
        #自定义保存数据
        self.items=[]
    def __iter__(self):
        mylist=MyListIterator(self.items)
        return mylist
    def addItem(self,data):
        #追加保存数据
        self.items.append(data)
        print(self.items)

#自定义迭代器类：
class MyListIterator(object):
    def __init__(self,items):
        self.items=items
        self.current_index=0

    def __iter__(self):
        pass
    def __next__(self):
        if self.current_index<len(self.items):
            data= self.items[self.current_index]
            self.current_index+=1
            return data
        else:
            raise StopIteration #主动抛出异常 停止迭代


if __name__ == '__main__':
    #创建自定义列表对象
    mylist =MyList()
    mylist.addItem("鲁班")
    mylist.addItem("张飞")
    mylist.addItem("吕布")
    for value in mylist:
        print(value)

    mylist_iterator = iter(mylist)
    value =next(mylist_iterator)
    print(value)