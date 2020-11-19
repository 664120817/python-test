import random,time
import numpy as np
# ndarray与 python原生态运算 对比
# 生成一个大数组
# lists=[]
# for i in range(1000000):
#     lists.append(random.random())
# ndarray_lists=np.array(lists)
# print(len(ndarray_lists))
# t1 =time.time()
# a=sum(lists)
# t2=time.time()
# d=t2-t1
#
# t3=time.time()
# b=np.sum(ndarray_lists)
# t4=time.time()
# d1=t4-t3
# print(d,d1)
#
# # ndarry的属性
# y=np.array([[3,12,10],[9,2,67],[2,0,11]])
# print(y.shape)
# print(y.ndim)#维度
# print(y.size)#多少个元素
# print(y.dtype)#类型
# x=np.array([[3,12,10],[9,2,67],[2,0,11]],dtype='float64')
# print(x,x.dtype)

# #生成0和1的数组
# a =np.zeros(shape=(3,4),dtype='float32')
# b =np.ones(shape=(3,4),dtype='int32')
# print(a,b)
# c=np.full(shape=(3,4),fill_value=1024) #fill_value 可以建立任何数
# print(c)
#
# #从现有数组生成
# # np.array()#拷贝
# # np.asarray() #深拷贝
# # np.copy() #浅拷贝  # numpy运算直接改变了原数组，如果不想改变上层数组 np.copy() 进行运算
# #生成固定范围的数组
# np.linspace(0,10,100) #生成0到10内  等距离100个数字
# np.arange(0,10,2) #和python中arange用法一样  2时步长
# #生成随机数组
# np.random.randint(0,100,10) #随机生成0-100 中的10个数
# np.random.uniform(low=-1,high=1,size=1000) #均匀分布
# np.random.normal(loc=1.75,scale=0.1,size=100)#正态分布 np.random.random 也是正态分布

# #数组的索引 切片
# a1=np.random.normal(loc=0,scale=1,size=(8,10))
# print(a1,a1.shape)
#获取第一个股票前3个交易日的涨幅数据
# a2=a1[0,:3]
# print(a2)
# #创建一个3维数组
b1=np.array([ [[1,2,3],[9,7,5]],[[2,3,4],[2,5,7]]])
print(b1,b1.shape)
b1[1,0,2]=888
print(b1)
# 排序算法
b1.sort() #原来的数据进行了改变，不占内存
print(b1)
b1=np.array([ [[55,1,2,3],[66,9,7,5]],[[88,2,3,4],[19,2,5,7]]])
b2=np.partition(b1,-1) # 负数为提取最大几个数 后面显示  正数提取最小的几个数前面显示 没有排序
print(b2)

#形状修改
a1=np.random.normal(loc=0,scale=1,size=(8,10))
print(a1,a1.shape)
aa=a1.reshape(10,8)#把8行10列 改为 10行8列（只是修改形状，没有行列翻转）#可将3维转化成一维（10*8*2）
print(aa,aa.shape)
ab=a1.resize(10,8) #没有返回值，对原始数组进行了修改  (也只改变了形状）
ac=a1.T #转置  行变列 列变行

#类型修改
b1=np.array([ [[1.0,2.0,3],[9,7,5]],[[2,3,4],[2,5,7]]])
b2=b1.astype('int32')#转化成整形32
b3=b1.astype('float64') #转化为浮点型64
print(b2)
# b2.astype(b3.dtype) 把b2类型改为b3一样的类型
#序列化到本地
b4=b1.tostring()
print("b4:",b4)

#数组的去重
b1=np.array([ [[1.0,2.0,3],[9,7,5]],[[2,3,4],[2,5,7]]])
bb=np.unique(b1) #去重变一维[1. 2. 3. 4. 5. 7. 9.]
print(bb)
#set去重必须为1维
set(b1.flatten()) #flatten()将数组变为一维
