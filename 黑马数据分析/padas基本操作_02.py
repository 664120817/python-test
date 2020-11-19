import numpy as np
import pandas as pd
data=pd.read_excel(r"C:\Users\Administrator\Desktop\数据\阳泉餐厅1.xlsx")
# print(data)
data=data.drop(["链接","地址:","营业时间:"],axis=1) #data.drop去掉不要的索引列     del data['链接'] 删除掉这列
print(data)

#索引操作
#1，直接索引 ， 先列后行
a=data["店名"][1]
print(a)
#2,间接索引，不分行列，按名字索引
b=data.loc[5]["电话："]
print(b)
#按数字索引
c=data.iloc[2,2]
print("c:",c)
#4组合索引
d=data.loc[data.index[:4]],[data.columns[:4]]  #iloc 和loc区别       loc 是标签索引       iloc 是数字索引
# d = data.iloc[:,:4][data.评分 >4]
print("d:",d)

#赋值操作 多重索引loc[(),()]
data["店名"]="美团" #索引值 全部赋值
data.iloc[0,0] = "新赋值" #单个赋值
# data.iloc[1:6,0]='饿了么'  #多个赋值
print(data)
#删除值 data.dorp(['20','21'],axis=index) #axis =columns   inplace=True 在原始文本中dorp
#排序
data2=data.sort_values(by="人均：",ascending=False) #ascending=False 降序  ascending=True 升序 默认是升序
# print(data2)
#多个序列排序
data3=data.sort_values(by=["人均：","评分"],ascending=False) #先看人均 人均相同 看评分  #nan会排序最后
print("data3:",data3)
#按索引进行排序
# dd = data.sort_index(axis=1) #ascending=False 降序  ascending=True 升序 默认是升序
# print("dd",dd)
# rank 位置排序 返回排序后的位置序号
r =pd.Series([7,1,6,5,4,6])
print(r.rank(method='first')) #rank() 更多用法去百度

#对时间数据转换date = pd.to_datetime(['数据])  在排序date.sort_values(by='时间数据')

f = open(r"C:\Users\Administrator\Desktop\数据\宝马3.csv")
data=pd.read_csv(f,usecols=['名字','年限','价格','公里','售价'])
print(data)
data_x=data.set_index('名字')
print(data_x)


