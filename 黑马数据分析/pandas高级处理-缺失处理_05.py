import pandas as pd
import numpy as np
#pandas高级处理
f = open(r"C:\Users\Administrator\Desktop\数据\宝马3.csv")
data=pd.read_csv(f,usecols=['名字','年限','价格','公里','售价'],na_values=['NULL']) #na_values= ['NULL'] 把[]内的值设置为 NaN 去除奇怪字符 为NaN
# print(data)
#如何处理nan  判断数据中是否存在nan
data_qs=pd.isnull(data) #isnull 如果是缺失值为True 不是为Fasle  等同data_qs=data.isnull()
# data_qs=pd.notnull(data) #notnull 如果是缺失值为Fasle 不是为True 用np.all 判断缺失值
# print(data)
data_n=np.any(data_qs) #np.any 有一个True 返回True 说明有缺失值
print("data_n:",data_n)
data_p=data_qs.any() #返回每一个索引的bool值是否含有缺失值 any(axis = 0)
print("data_p:",data_p)
#缺失值处理 1，删除含有缺失值的样本  dropna(how='all') #所有值为NaN才被删除    dropna(thresh = 2) 2 只删除前2行
data1=data.dropna(inplace=False) #dropna() 删除含有缺失值的样本 加参数inplace=True 在原始文本中修改  inplace=False 重建一个新的文本  默认按行删除
# print(data1)
# 2，替换、插补 #data['公里'].fillna（data['公里'].mean,inplace=Flase）
# data.fillna(method='ffill', inplace=True)  # 向前填充              bfill / backfill向后或进位填充    limit=2 只填2个
# data2=data.fillna("填补的缺失值",inplace=True)#data.fillna(value,inplace=True) value是要填补的值建议用平均值 分位数 参数inplace=True 在原始文本中修改  inplace=False 重建一个新的文本
# print("data2:",data)                 #data2.fillna({data['名字']:'宝马',data['年限']:2020})
print('6666',data.fillna({'名字':'宝马','年限':'2020'})) #给对应列的填补
#不是缺失值nan，有默认标记的
#1，替换[] 为np.nan  data.replace(to_replace='[]',value=np.nan) to_replace要替换的字段  value替换成想要的数据
data3=data.replace(to_replace='[]',value = np.nan)
# print(data3)
#删除重复数据
data_s=data.duplicated() # 以每行对比 如果相同就返回Ture    data.duplicated(['名字']) 对某一列进行对比
data_s.drop_duplicates() # 调用 data_s.drop_duplicates() 删除相同数据  data_s.drop_duplicates(subset=[索引1，索引2]) #根据索引相同的删除
print(data_s)
data3.dropna(inplace=True) #删除替换后的nan空字段 data3.dropna(how='all')#所有值为空才被删除  data3.dropna(subset=[索引1，索引2]，how='all'，axis='') 根据索引删除
print(data3,data3.isnull().any() )
#data[''].str.lower() 统一某一列的大小写
#a.combine_first(b) 类同np.where(pd.isnull(a),b,a)     表1.combine_first（表2） 让表2对应填充表1的nan

#数据离散化 如何实现数据离散化
# 1，分组 自动分组 sr=pd.qcut(data,bins)#(分组的数据，组数)
#自定义分组 sr=pd.cut(data,[])#(分组的数据，以列表形式传入分组区间)
#2,将分组好的结果转化one-hot编码
# pd.get_dummies(sr,prefix=) #prefix前缀

#准备数据
da=pd.Series([165,174,160,180,159,163,192,184],index=['No1:165','No1:174','No1:160','No1:180','No1:159','No1:163','No1:192','No1:184'])
print(da)
#分组 自动分组   #cut将根据值本身来选择箱子均匀间隔，qcut是根据这些值的频率来选择箱子的均匀间隔。
sr=pd.qcut(da,3)#(分组的数据，组数)   precision=2 限定小数点为2位  (da,[按自定百分比])
counts=sr.value_counts() #查看每个分组区间有多少人
print("sr:",sr,"counts:",counts)
da1=pd.get_dummies(sr,prefix="height") #离散化处理
print("da1:",da1)
#自定义分组
bins=[150,165,180,195]
sr1=pd.cut(da,bins)  #right =Flase 右边为开区间，左边为闭区间  labels=[] 给每个区间一个名称
#print(sr1.codes) #查看每一个数 被分到了几组   sr1.categories 查看分组情况
counts=sr1.value_counts() #查看每个分组区间有多少人
print(sr1,counts)

#数据离散化处理
da2=pd.get_dummies(sr,prefix="身高")
print(da2)
#练习
data4=data['公里'].replace(to_replace='[]',value=np.nan)
data4.dropna(inplace=True) #删除替换后的nan空字段
data4=data4.astype('float64')
dataf=pd.qcut(data4,4)
counts=dataf.value_counts() #查看每个分组区间有多少人
print(dataf,counts)
datal=pd.get_dummies(dataf,prefix="公里")
print(datal)


#合并
#1,按方向拼接 pd.concat([data1,data2],axis=0) axis=0是竖直拼接   axis=1是水平拼接  ignore_index=Ture  合并后的行索引重新编序  keys=[]给原表取标签名 join ='outer'显示合并超出部分没有的nan补充 inplace=True
data4=data4.head(10)    # 表.stack()  将columns变成index成index双索引    表.unstack()  index双索引，打平行索引 ()填 0 1 或 name
datall=datal.head(10)
# pj=pd.concat([data4,datall],axis=1 )#,join_axes=[[]] 指定要合并的索引行
pj=pd.concat([data4,datall],axis=1)#是水平拼接   #(dataf[['']].join(data1)) 把需要的数据和离散化数据拼接起来
print("pj",pj)
#按索引拼接  pd.merge实现合并  pd.merge（表1,表2,how='inner',on=['索引']）how 代表以内连接 还是外连接 on以那些索引连接           left_index =True按左索引合并很少用到
# pd.merge(表1,表2, 表1='索引', 表2_index=True) #表1 索引 和 表2 行索引合并
# 表1.join（表2,how='inner',on=['索引']）
# 请参考链接 https://www.cnblogs.com/keye/p/10791705.html


#交叉表与透视图  找到，探索两个变量之间的关系 pd.crosstab(value1,value2)  参考：https://www.cnblogs.com/dataAnalysis/p/9371439.html  网址里解释更清晰
stock=pd.read_html('http://app.finance.ifeng.com/data/stock/stock_daily3.php?code=sh600810&begin_day=2019-08-23&end_day=2019-10-14',index_col= 0, header= 0)[0]
print("stock:",stock,"stock.index:",stock.index)
#pandas日期类型 有助于转化年 月 日 星期的类型
date=pd.to_datetime(stock.index)
print("date.weekday:",date.weekday) #获取星期
#将星期几添加列表后面
stock['week']=date.weekday
print(stock)
#准备涨跌幅数据列 添加到stock列表 后
stock['pona']=np.where(stock['涨跌额']>0,1,0)
print(stock)
#交叉表 对比 星期天与涨跌幅的关系
data5=pd.crosstab(stock['week'],stock['pona'])
print("data5",data5)
#球涨幅数量的百分比
data5s=data5.sum(axis=1)#以行相加
print('data5s',data5s)
data5ss=data5.div(data5s,axis=0) #以列相除
print(data5ss)
#画图
import matplotlib.pyplot as plt
#交叉表
data5ss.plot(kind='bar',stacked='True')#kind='bar' 画柱状图  stacked='True' 是否堆叠显示
plt.show()
#使用pivot_table（透视表）
data6=stock.pivot_table(['pona'],index=['week']) #按index=['week'] 分组
print('data6',data6)

#data.take(5) 随机抽取5个样本
#分组与聚合
df=pd.DataFrame({'key1':['a','a','b','b','a'],
             'key2':['one','two','one','two','one'],
             'data1':np.random.randn(5),
             'data2':np.random.randn(5)})
print(df)
#对key1进行分组 data1进行聚合
df1=df.groupby(by='key1')['data1'].max()#by 按那个索引进行分组 ['data1'].max() 聚合最大值 df1=df.groupby(by='key1')['data1'].sum()['a']
print(df1)
#案列
f = open(r"C:\Users\Administrator\Desktop\数据\esfhourse.json",'rb')
f1=pd.read_json(f,orient='records',lines=True)
print(f1)
#均价
p=f1['totalprice'].mean()
print(p)
#小区个位数
dd=np.unique(f1['commname']).size #unique去除数组中的重复数字，并进行排序之后输出。
print(dd)
#对于 totalprice 的分布情况，应该如何呈现数据
#pandas绘图
h=f1['totalprice'].plot(kind='hist')
plt.show()
#matplotlib绘图
plt.figure(figsize=(10,8),dpi=80)
plt.hist(f1['totalprice'],10)
plt.xticks(np.linspace(f1['totalprice'].min(),f1['totalprice'].max(),10)) #np.linspace主要用来创建等差数列
# 添加网格显示
plt.grid(True,linestyle="--",alpha=0.5) #linestyle 线条风格  ,alpha 透明度
plt.show()

# #透视表
# pd.pivot_table(df,index=[u'主客场',u'胜负'],values=[u'得分',u'助攻',u'篮板'],aggfunc=[np.sum,np.mean])  #类似index分组，values 要提取的值，aggfunc 分组后要求的值 columns=[]