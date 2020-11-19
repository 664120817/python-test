import numpy as np
import pandas as pd
datas=np.random.normal(0,1,(10,5))
#添加行索引
stock=["股票{}".format(i) for i in range(10)]
print(stock)
#添加索引日期
date=pd.date_range(start="20180101",periods=5,freq="B")
print(date)
data_p=pd.DataFrame(datas,index=stock,columns=date)# ndex=stock添加行索引 columns=date添加列索引
print(data_p.columns)
#DataFrame的属性
data1=data_p.shape
data2=data_p.values
data3=data_p.T
h=data_p.index #获取行索引
l=data_p.columns#获取列索引
print(h,l)
data_p.head() #默认是获取前5条内容
data_p.tail()#默认是获取后5条内容

#DataFrame索引的设置
#修改行列索引值
# hs=data_p.index[2] = "股票二"  不能单独修改索引   data.rename()
stock_=["股票_{}".format(i) for i in range(10,20)]
data_p.index=stock_
print(data_p)
#重设索引 data_p.reset_index()重设新的索引，不想保留原来的index，使用参数 drop=True         as_index =False  不使用index当索引  自动生成一个新的索引
data_p.reset_index(drop=False) #False 不删除原来索引 True 删除原来索引           reset_index()#默认drop=False  获得新的index，原来的index变成数据列保留下来  (drop=True)不保留原来的index
#设置新行索引
date_x=pd.date_range(start="20190101",periods=5,freq="B")
data_xx=data_p.set_index(["2018-01-05","2018-01-02"]) #将"2018-01-05","2018-01-02"列  变成index双索引  添加drop=False参数来保留数据
print("data_xx",data_xx,data_xx.values) # 表.stack()  将columns变成index成index双索引    表.unstack()  index双索引，打平行索引 ()填 0 1  或 name

# Multilndex 索引对象
data_name=data_xx.index.names #获取索引名
print(data_name)
data_con=data_xx.index.levels #获取索引对应的内容
print(data_con)

#跟换所有
# date.index=["要更换的索引列表"]
# data.rename(index=index,columns=columns) # 也是更换索引   #data.rename(columens={'索引1':name,'索引2':name2},in)单个索引更换

#Panel 是DataFrame的容器place=Ture
#Series 结构只有行索引 带索引的一维数组  DataFrame是Series的容器

#数据汇总工具
df=pd.DataFrame({'sex':['male','female','female','male'],
                        'smoke':['Yes','No','No','No'],
                        'height':np.random.randint(158,188,4),
                        'weight':np.random.randint(50,80,4)})
print("df\n",df)
#行分组透视图
df1=df.pivot_table(index="sex") #添加参数 aggfunc=max
print("df1\n",df1)
#行列分组的透视表
df2=df.pivot_table(index="sex",columns='smoke')
print("df2\n",df2)

obj = pd.DataFrame(np.arange(16).reshape((4,4)),index=['one','two','three','four'],columns=['a','b','c','d'])
round1= lambda x: x+10
obj1=obj.applymap(round1)
# obj1=obj['a'].map(round1)
print(obj)
print("8888888888",obj1)