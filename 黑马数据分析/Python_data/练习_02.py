import pandas as pd
import numpy as np
#数据透视表  宽表变长表
data =pd.read_csv(r'C:\Users\Administrator\Desktop\数据\pydata-book-2nd-edition\examples\macrodata.csv')
print(data.head())
periods = pd.PeriodIndex(year=data.year, quarter=data.quarter,name='date') #pandas之时间序列(data_range)、重采样(resample)、重组时间序列(PeriodIndex)
columns = pd.Index(['realgdp', 'infl', 'unemp'], name='item')
print(periods)
data = data.reindex(columns=columns) #.reindex挑选  插值
print(data)
data.index = periods.to_timestamp('D',how='start') #转为日期  D代表天    'end' 代表最后结束值
print(data.index)
print(data.head())
# print(data.stack().head())
ldata = data.stack().reset_index().rename(columns={0: 'value'})  # stack()列索引变行索引 reset_index()重设新的索引  rename(columns={0: 'value'}改索引名
print(ldata[:10])

#长表变宽表
print("555555555",ldata.set_index(['date', 'item']).unstack('item').rename(columns={'value':"" }),"5555555555555")
pivoted = ldata.pivot('date', 'item','value') #通过指定的index/column values 来对DataFrame进行重塑。 不支持数据聚集
print(pivoted.head())
ldata['value2'] = np.random.randn(len(ldata))
print(ldata[:10])
pivoted = ldata.pivot('date', 'item') #通过指定的index/column values 来对DataFrame进行重塑。 不支持数据聚集
print(pivoted[:5])
print(pivoted['value'][:5])
unstacked = ldata.set_index(['date', 'item']).unstack('item') #等同ldata.pivot('date', 'item') 的效果
print(unstacked[:7])

# 宽表变长表
df = pd.DataFrame({'key': ['foo', 'bar', 'baz'],
                   'A': [1, 2, 3],
                   'B': [4, 5, 6],
                   'C': [7, 8, 9]})
print(df)
melted = pd.melt(df, ['key']) # 根据['key'] 这一列来做分组
print(melted)
reshaped = melted.pivot('key', 'variable', 'value')
print(reshaped)
print(reshaped.reset_index())
pd.melt(df, id_vars=['key'], value_vars=['A', 'B'])  #根据['key'] 这一列  只拿['A', 'B'] 两列做分组
pd.melt(df, value_vars=['A', 'B', 'C'])   #不指定id_vars=['key']  来做分组
pd.melt(df, value_vars=['key', 'A', 'B'])


import matplotlib.pyplot as plt
from datetime import datetime

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

data = pd.read_csv(r'C:\Users\Administrator\Desktop\数据\pydata-book-2nd-edition\examples\spx.csv', index_col=0, parse_dates=True) # index_col=0 设置第一列为index值 parse_dates=True 时间分开出来
spx = data['SPX']

spx.plot(ax=ax, style='k-')
# Zoom in on 2007-2010
ax.set_xlim(['1/1/2007', '1/1/2011'])
ax.set_ylim([600, 1800])

crisis_data = [
    (datetime(2007, 10, 11), 'Peak of bull market'),
    (datetime(2008, 3, 12), 'Bear Stearns Fails'),
    (datetime(2008, 9, 15), 'Lehman Bankruptcy')
]
for date, label in crisis_data: #date日期   label标注
    ax.annotate(label, xy=(date, spx.asof(date) + 75), #spx.asof(date)  spx 位于date 时间的数据 +75 标注写在此上面75的位置
                xytext=(date, spx.asof(date) + 225),
                arrowprops=dict(facecolor='black', headwidth=4, width=2,
                                headlength=4),
                horizontalalignment='left', verticalalignment='top')
ax.set_title('Important dates in the 2008-2009 financial crisis')
plt.show()

#画圆形 三角形 长方形
fig = plt.figure(figsize=(12, 6)); ax = fig.add_subplot(1, 1, 1)
rect = plt.Rectangle((0.2, 0.75), 0.4, 0.15, color='k', alpha=0.3)
circ = plt.Circle((0.7, 0.2), 0.15, color='b', alpha=0.3)
pgon = plt.Polygon([[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]],
                   color='g', alpha=0.5)
ax.add_patch(rect)
ax.add_patch(circ)
ax.add_patch(pgon)
plt.axis('equal') #让x,y刻度长度相同
plt.show()

#以什么格式保存  plt.savefig('figpath.svg')  plt.savefig('figpath.pdf')  plt.savefig('figpath.png', dpi=400, bbox_inches='tight')

fig, axes = plt.subplots(2, 1)
data = pd.Series(np.random.rand(16), index=list('abcdefghijklmnop'))
data.plot.bar(ax=axes[0], color='k', alpha=0.7)
data.plot.barh(ax=axes[1], color='k', alpha=0.7)
np.random.seed(12348)
df = pd.DataFrame(np.random.rand(6, 4),
                  index=['one', 'two', 'three', 'four', 'five', 'six'],
                  columns=pd.Index(['A', 'B', 'C', 'D'], name='Genus'))
print(df)
df.plot.bar()
plt.figure()
df.plot.barh(stacked=True, alpha=0.5)
plt.show()

#交叉表是用于统计分组频率的特殊透视表   https://blog.csdn.net/elecjack/article/details/50760736
tips = pd.read_csv(r'C:\Users\Administrator\Desktop\数据\pydata-book-2nd-edition\examples\tips.csv')
party_counts = pd.crosstab(tips['day'], tips['size'])  # 按tips['day']分组，统计tips['size']分组中出现频数
print(party_counts)
# Not many 1- and 6-person parties
party_counts = party_counts.loc[:, 2:5]
party_pcts = party_counts.div(party_counts.sum(1), axis=0) #div 除以
print(party_pcts)
party_pcts.plot.bar()
plt.show()