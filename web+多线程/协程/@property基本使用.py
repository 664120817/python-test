class Goods(object):
    #初始化方法
    def __init__(self):
        self.org_price =1000
        self.discount = 0.7

    #获取价格的方法
    @property
    def price(self):
        return  self.org_price*self.discount

    #设置价格的方法
    @price.setter
    def price(self,val):
        self.org_price =5000
    @price.deleter
    #删除价格方法
    def price(self):
        print("执行了删除方法")



#创建对象
good =Goods()
print(good.price) #同等good.price == good.price()

good.price =500 #同等 good.price(500)
print(good.price)

del good.price