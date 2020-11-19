import numpy as np
#逻辑运算
# a1=np.random.normal(loc=0,scale=1,size=(8,10))
# print(a1>0) #显示为bool值，大于0为True ,小于0为False
# a1[a1>0]=1 #把所有大于0 的值赋值为1
# print(a1)
#
# #通用判断函数
# np.all(bool) #只要有一个False就返回False,全是True 返回True
# np.any(bool) #只要有一个True就返回True,全是False 返回False
#
#三元运算符
# a1=np.random.normal(loc=0,scale=1,size=(8,10))
# print(a1)
# a2 =a1[:4,:4]
# np.where(a2>0,1,0)#where(bool,true,fasle) 把true变为1 ,fasle变为0
# np.logical_and(a1>1,a1<-1) # 类同 a1>1 and a1<-1
# np.logical_or(a1>1,a1<-1) #类同 a1>1 or a1<-1
# print(np.where(np.logical_and(a1 > 1, a1 < -1), 1, 0)) #判断Ture 返回1 Fasle 返回 0
#
# #统计运算
# a1=np.random.normal(loc=0,scale=1,size=(8,10))
# a2=a1[:4,:4]
# b1=np.max(a1,axis=0) #每列中的最大值
# b2=np.max(a1,axis=1)#每行中的最大值
# b3=np.argmax(a1,axis=1) # argmax 最大值所在的索引位置
# #np.argwhere

#数组间的运算
#数组与数字运算
arr = np.array([[1,2,3,2,1,4],[5,8,7,9,11,14]])
arrs=arr+10 #对数组每一个元素加10
print(arrs)
#数组与数组的运算 使用了广播机制
arr1=np.array([[5,4,6,8],[4,5,2,1]])
print(arr.shape)#(a,b)
print(arr1.shape)#(cd)
#若a c相比 a=c 或a c其中一个为1 b d相比 b=d 或b d其中一个为1 则可以运算 arr和arr1不能运算

#矩阵运算
#ndarray 存储矩阵
jz=np.array([[82,85],[88,78],[66,74],[85,75],[72,66]])
#matrix存储矩阵
jzm=np.mat([[82,85],[88,78],[66,74],[85,75],[72,66]])
#矩阵相乘形状条件:  (M行，N列)*(N行,L列)=(M行,L列)
jm=np.mat([[1],[2]])
print(jzm.shape,jm.shape)
#矩阵运算
# res=np.matmul(jzm,jm)
res=jzm*jm
print("res",res)

#合并，分割的用处
a=np.array([[1,2,3,4],[11,22,33,44]])
b=np.array([[5,6,7,8],[55,66,77,88]])
#水平拼接
absp=np.hstack((a,b)) #水平合并 另一种方法np.concatenate((a,b),axis=1)
print(absp)
#竖直拼接
absz=np.vstack((a,b)) #竖直合并 另一种方法np.concatenate((a,b),axis=0)
print(absz)
#分割
x=np.array([0,1,2,3,4,5,6,7,8,9,10,11])
xf=np.split(x,3)#分成3份
xs=np.split(x,[1,5,6,10]) #以索引值划分  np.split(x,(3,5)) 切分2维数组会以行切分
print(xf)
# print(xs)
values =np.array([1,2,3,4,5,6])
values1 = np.array([4,5,6])
print(np.in1d(values,values1))  #values 有和values1 相同的返回Ture ,没有返回Flase  相当于交集 返回bool值
#Numpy读取 我们一般不用numpy读取数据 读取不了字符串
# data=np.genfromtxt("test.csv",delimiter=",")#读取test.csv文件，以,分割

#傅里叶
import numpy as np
from numpy.fft import fft,ifft #fft傅里叶转换 ifft傅里叶反转
from PIL import Image
girl =Image.open("girl.jpeg")
# girl.show()
#转换成int 类型
girl_data=np.fromstring(girl.tobytes(),dtype=np.int16)
#傅里叶转换
girl_data_fft = fft(girl_data)
print(girl_data_fft)
#自定一个频率，小于这个频率为低频率，将低频率设置为0
girl2=np.where(np.abs(girl_data_fft)<1000000000,0,girl_data_fft)
print(girl2)
# 3使用傅里叶反转
girl_data_ifft=ifft(girl2)
print(girl_data_ifft)
#获取实数
girl_data_real=np.real(girl_data_ifft)
print(girl_data_real)
girl_data_result=np.int16(girl_data_real) #除去小数点
#转化成图片
girl_Image=Image.frombytes(data=girl_data_result,mode=girl.mode, size=(10,8))
# girl_Image.show()
