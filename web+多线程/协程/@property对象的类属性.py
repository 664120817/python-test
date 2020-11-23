class Goods(object):
    #初始化方法
    def __init__(self):
        self.org_price =1000
        self.discount = 0.7

    #获取价格的方法
    def get_price(self):
        return  self.org_price*self.discount

    #设置价格的方法
    def set_price(self,val):
        self.org_price =5000
    #删除价格方法
    def del_price(self):
        print("执行了删除方法")

    BAR=property(get_price,set_price,del_price,"BAR是一个porperty 对象")

    #魔术方法
    def __call__(self, *args, **kwargs):
        print("__call__方法被调用") #good()  调用

    def __del__(self):
        print("__del__ 正在执行") #del good  调用

    def __str__(self):
        return  "我是一个寂寞对象"


    def __getitem__(self, item):
        print("key=",item) #good['a']调用

    def __setitem__(self, key, value):
        print("key={},value={}".format(key,value))
    def __delitem__(self, key):
        print("要删除 key =",key)


#创建对象
good =Goods()
print(good.BAR) #同等good.price == good.price()

good.BAR =500 #同等 good.price(500)
print(good.BAR)

del good.BAR

print(Goods.BAR.__doc__)
print(Goods.__dict__)

print(good.set_price.__doc__) #对象方法的描述
print(good.__module__) #获取当前模块
print(good.__class__) # 获取当前对象信息


good() #对象名直接调用
print(good) #打印对象时默认输出
# del good  #删除对象

good['a'] #调用 __getitem__ 方法
good['a'] =100 #调用 __setitem__ 方法
del good['a']#调用 __delitem__ 方法