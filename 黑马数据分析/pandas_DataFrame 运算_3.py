import pandas as pd
import numpy as np
import pymysql
f = open(r"C:\Users\Administrator\Desktop\数据\宝马3.csv")
data=pd.read_csv(f)
data=pd.DataFrame(data).head(10)
data['公里']=data['公里'].astype('float64') #astype 转化为浮点型64
data['售价']= data['售价'].astype('float64')
print(data)  #c =pd.get_dummies(data)   数字列自动提前，字符列离散化

#算法运算
data1= data['公里']
print(data1)
data2=data1*100
print(data2)
#逻辑运算
data1= data['公里']
datas= data['售价']
data3=data1 < 5 #返回一个bool值
print(data3)
data4=data[data1>5] #返回大于5的data数据
print(data4)
data5=data[((data1 < 5) & (datas < 19))] #组合 &代表并且 |代表或
print("data5:",data5)
data6=data.query("公里 < 5 & 售价 < 19") #与上面是同一种写法
print(data6)
#判断 "公里" 是否为 5.4，2.5
data7=data["公里"].isin([5.4,2.5]) #显示bool值
data8=data[data7].iloc[3::]
print(data8)

#统计运算
data_1=data.describe()
print("data_1:",data_1)
data_11=data['售价'].max(axis=0) #axis=0列的最大值 axis=1 行的最大值
data_12=data['售价'].idxmax(axis=0) #返回最大值所在的索引位置 ata.idxmin() #返回最小值所在的索引位置
print(data_11,data_12)
#map函数运算
def jia(item):
    if item > 20:
        return  item +10
    else:
        return 0
data['售价']=data['售价'].map(jia) #map()内为一个函数 把前面元素传入map(）函数内调用
print(data["售价"],"66666")

#累计统计函数
import matplotlib.pyplot as plt
# data_=data['售价'].sum(fill_value=0)# 求和 当有空值时 用fill_value值  替代
data_2=data['售价'].cumsum() #累加
print(data_2)
data_3=data_2.plot() #画图
plt.show()

#自定义运算  data.describe(include = [索引]) 对字符串的统计  include =all 所有的字符串统计
# data_4=data.apply(lambda x:x.max()-x.min(),axis=0) #  最大值 - 最小值 axis=0按列
data_5=data["售价"].max()-data["售价"].min()
print(data_5)

#画图
datat=data.plot(x='公里', y='售价',kind='scatter',title = '二手车') #kind 代表画什么图
plt.show()
print(datat)
#多数据画图
df=pd.DataFrame(np.random.randint(0,30,size = (10,4)),index=list('abcdefghil'),columns=list('ABCD'))
print(df)
df.plot(title="数据") #kind='bar'柱状图
plt.show()
#散布图矩阵，当有多个点时，两两点的关系
pd.plotting.scatter_matrix(df,diagonal = 'kde')
plt.show()

# def draw(deck, n=5):   #随机抽取5个样本 不放回
#     return deck.sample(n)
# print(draw(data))

import matplotlib
# print(matplotlib.matplotlib_fname()) #查询模块目录  np.sign（data）将正数变1  负数变-1


#相关系数
print(data['公里'].corr(data['售价'])) #相关系数    data.corrwith(data.公里)求公里和每一个列的相关系数
# coun =pymysql.Connect(host="localhost", port=3306, user="root", passwd="4786874", db="spider", charset="utf8")
# Data = pd.read_sql('select jz1,jy1,jy3,jy6 from jjph',coun)
# Data=pd.DataFrame(Data,dtype=np.float).head(10)
# print(Data['jz1'].corr(Data['jy1']))
# print(Data.corr()) #求所以相关系数    Data.cov 协方差矩阵
# print(Data.corrwith(Data.jz1)) #与jz1的所有相关系数
