import  pandas as pd
import json,numpy as np
import os
os.getcwd() #获取当前路径
os.chdir(r'C:\Users\Administrator\Desktop\数据') #切换路径
# print(os.getcwd())
#读取Excel
# data = pd.read_excel(r"C:\Users\Administrator\Desktop\数据\武汉新盘.xlsx", sheet_name = 1) #  sheet_name 第几个工作表，也可以写表名
#读取csv文件  index_col =0  第一列作为index索引
f = open(r"宝马3.csv")
data=pd.read_csv(f,usecols=['名字','公里','售价'],encoding='utf-8')#usecols选择读取的索引 可以用参数sep="" 进行分割    index_col=['名字','售价'] 提取列 当index 可多个索引 dtype={'售价':'float'} 以浮点数类型读取
# print(data)
# print(data.info())  #归纳信息
#如果没有索引值  用参数names添加
# data1=pd.read_csv(f,usecols=['名字','年限','价格','公里','售价'],names=['名字','年限','价格','公里','售价'])#usecols选择读取的索引
# print(data1)
#os.remove(文件名) 移除文件
#保存 '售价'列的数据
data2=data[:10] #类同data.head(10)
print("data2:",data2)
print(data.info())
data2.to_excel('test.xlsx',columns=['售价'],index=False) #columns代表要保存的列 index=Fals不要行索引  header =Fals 不要列索引
# data2.to_excel('test.xlsx',columns=['售价'],index=False,mode='a',header=False)#mode以什么模式写入 header=False写入时不追加索引图

#保存到HDF5
# f = pd.DataFrame({'a':np.random.randn(100)})
# store = pd.HDFStore('mydata.h5')
# store['data'] =f
# store['data_col'] =f['a']
# print(store['data'],store['data_col'])
# store.close()
# HDF5文件读取 hdf5 存储3维数据的文件
# data3= pd.read_hdf('path')
#保存
# data3.to_hdf('path',key='close')
#hdf5可能有多个键 下次读取要添加键  pd.read_hdf('path',key='close')

#JSON读取
f1 = open(r"esfhourse.json",'rb')
data4=pd.read_json(f1,orient='records',lines=True)#orient以什么形式展现，lines是否以行读取
print(data4)
#保存
data4.to_json('test.json',orient='records',lines=True)#orient以什么格式存储，lines每一行存储一次

dates = pd.date_range("20180301", periods=8)
df = pd.DataFrame(np.random.randn(8, 5), index=dates, columns=list('ABCDE'))  # randn正态分布中随机数#
print (df)
df1 = df.reindex(index=dates[:4], columns=list("ABCD") + ["G"])#reindex()数据符合新的索引来构造一个新的对象
print(df1)
# 使它符合新的索引，如果索引的值不存在就填入缺失值 #
# method：插值填充方法method: {None, ‘backfill’ / ’bfill’, ‘pad’ / ’ffill’, ‘nearest’} #
# ffill / pad向前或进位填充，bfill / backfill向后或进位填充 #
# #reindex可以改变（行）索引，列或两者。当只传入一个序列时，结果中的行被重新索引，使用columns可以将列进行索引#
# fill_value：引入的缺失数据值；limit：填充间隙；如果新索引与旧的相等则底层数据不会拷贝。默认为True(即始终拷贝)；
#level：在多层索引上匹配简单索引




