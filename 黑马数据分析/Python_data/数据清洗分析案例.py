import numpy as np
import pandas as pd
from scipy import stats
import os
os.chdir(r'C:\Users\Administrator\Desktop\数据')
f = open(r"宝马3.csv")
BOM=pd.read_csv(f,encoding='utf-8' ,dtype={'公里':'str'},usecols=['名字','年限','价格','公里','售价'])
#缺省值统计
BOM.replace(to_replace='[]', value=np.nan,inplace=True)
print(BOM)
print(BOM.apply(lambda x: sum(x.isnull()) / len(x), axis=0)) #查看空值率
df =BOM.dropna(how='any').copy() #删除缺失值  且拷贝
df['年限'] =df['年限'].str[:4]   #date.diff(1)计算日期    上一个值减下一个值
print(df['年限'])
df['年限'] =pd.to_datetime(df['年限'],errors='coerce') #errors='coerce' 容错处理，发生错误直接去除
df['年限'] =df['年限'].dt.date #提取年日期               d.describe(include = [索引]) 对字符串的统计  include =all 所有的
print(df)
import  plotly as py
df1=df.groupby('年限').count()
print(df1)
import plotly as py
import plotly.graph_objs as go

trace_tip = go.Bar(x=df1.index.values,
                    y=df1['名字'].tolist(),
                       # mode='markers+text',
                       # mode决定图上出现点，线，text等的组合形式
                       name='宝马出售数量图',

                   )

# plotly.offline.plot(dict(data=[trace_tip]),filename='plot.html')
fig = go.Figure(data=[trace_tip])
# 如果在这个基础上接着画，那就[trace_tip1, trace_tip2...]
fig.show()