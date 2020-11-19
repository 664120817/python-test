import pandas as pd
import numpy as np

# df.groupby('key1')['data1'] df.groupby('key1')[['data2']]
# df['data1'].groupby(df['key1']) df[['data2']].groupby(df['key1']) 同上一样，写法不一样
# df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
#                    'key2' : ['one', 'two', 'one', 'two', 'one'],
#                    'data1' : np.random.randn(5),
#                    'data2' : np.random.randn(5)})
# print(df)
# grouped = df['data1'].groupby(df['key1'])
# # print("grouped:",grouped)
# # print(grouped.mean())
# means = df['data1'].groupby([df['key1'], df['key2']]).mean()  #先以前面df['key1']分组 在分后面的df['key2']
# print(means)
# # print(means.unstack())
# states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
# years = np.array([2005, 2005, 2006, 2005, 2006])
# df['data1'].groupby([states, years]).mean()
# print("1:",df.groupby('key1').mean())
# print(df.groupby(['key1', 'key2']).mean())
# print(df.groupby(['key1', 'key2']).size())
#
# for name, group in df.groupby('key1'):
#     print(name)
#     print(group)
# for (k1, k2), group in df.groupby(['key1', 'key2']):
#     print((k1, k2))
#     print(group)
# pieces = dict(list(df.groupby('key1'))) #将分组转化成字典
# print(pieces['b'])  #分组后取出b这组
# print(df.dtypes)
# grouped = df.groupby(df.dtypes, axis=1) #根据类型分组
#
# for dtype, group in grouped:
#     print(dtype)
#     print(group)
# # agg 聚合 agg(['mean','std','自定函数']) 可以求多个函数     df.agg({'data1':[np.max,'mean','std'],'data2':'sum'})
# grouped1 = df.groupby('key1')
# print(grouped1['data1'].quantile(0.9)) #.quantile(0.9) 求90%的分位数
# def peak_to_peak(arr):
#     return arr.max() - arr.min()
# print(grouped1.agg(peak_to_peak)) #agg 聚合 调用函数  agg(['mean','std','peak_to_peak'])  df.agg({'data1':np.max,'data2':'sum'}) 求df['data1']最大值和 df['data2']的总和
# print(grouped1.describe())

# # 根据index 长度进行分组
# people = pd.DataFrame(np.random.randn(5, 5),
#                       columns=['a', 'b', 'c', 'd', 'e'],
#                       index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
# people.iloc[2:3, [1, 2]] = np.nan # Add a few NA values
# print(people)
# mapping = {'a': 'red', 'b': 'red', 'c': 'blue',
#            'd': 'blue', 'e': 'red', 'f' : 'orange'}
# by_column = people.groupby(mapping, axis=1)
# by_column.sum()
# map_series = pd.Series(mapping)
# print(map_series)
# print(people.groupby(map_series, axis=1).count())
# print(people.groupby(len).sum())  #len  根据index 长度进行分组
# key_list = ['one', 'one', 'one', 'two', 'two']
# print(people.groupby([len, key_list]).min())
#
# #根据列 name分组   分组聚合
# columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'],
#                                     [1, 3, 5, 1, 3]],
#                                     names=['cty', 'tenor'])
# hier_df = pd.DataFrame(np.random.randn(4, 5), columns=columns)
# print(hier_df)
# print(hier_df.groupby(level='cty', axis=1).count())


frame = pd.DataFrame({'data1': np.random.randn(1000),
                      'data2': np.random.randn(1000)})
quartiles = pd.cut(frame.data1, 4)
print(quartiles)
# print(quartiles[:10])
def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}
grouped = frame.data2.groupby(quartiles)
# print(grouped.apply(get_stats))
print(grouped.apply(get_stats).unstack())
# Return quantile numbers
grouping = pd.qcut(frame.data1, 10, labels=False) #labels=False  不显示分组标签
print(grouping)
grouped = frame.data2.groupby(grouping)
grouped.apply(get_stats).unstack()


s = pd.Series(np.random.randn(6))
s[::2] = np.nan #步长为2 设置为空
print(s)
s.fillna(s.mean())
states = ['Ohio', 'New York', 'Vermont', 'Florida',
          'Oregon', 'Nevada', 'California', 'Idaho']
group_key = ['East'] * 4 + ['West'] * 4
data = pd.Series(np.random.randn(8), index=states)
print(data)
data[['Vermont', 'Nevada', 'Idaho']] = np.nan
print(data)
data.groupby(group_key).mean()
fill_mean = lambda g: g.fillna(g.mean())  #函数
print(data.groupby(group_key).apply(fill_mean)) #调用函数
fill_values = {'East': 0.5, 'West': -1}
fill_func = lambda g: g.fillna(fill_values[g.name])   #以给定字典来填充
print(data.groupby(group_key).apply(fill_func))

#透视表   pivot_table 分组   有时更加方便快捷
#透视表  pd.pivot_table(df,index=[u'主客场',u'胜负'],values=[u'得分',u'助攻',u'篮板'],aggfunc=[np.sum,np.mean])  #类似index分组，values 要提取的值，aggfunc 分组后要求的值  columns=[]

#交叉表
from io import StringIO
data = """\
Sample  Nationality  Handedness
1   USA  Right-handed
2   Japan    Left-handed
3   USA  Right-handed
4   Japan    Right-handed
5   Japan    Left-handed
6   Japan    Right-handed
7   USA  Right-handed
8   USA  Left-handed
9   Japan    Right-handed
10  USA  Right-handed"""
data = pd.read_table(StringIO(data), sep='\s+')
print(data)
pd.crosstab(data.Nationality, data.Handedness, margins=True)

#练习
np.random.seed(12345)
draws = np.random.randn(1000)
# draws[:5]
bins = pd.qcut(draws, 4)
print(bins)
bins = pd.qcut(draws, 4, labels=['Q1', 'Q2', 'Q3', 'Q4']) #分组标签
print(bins)
print(bins.codes[:10])  #查看所在labels的位置
bins = pd.Series(bins, name='quartile')
print(bins[:10])  #labels的位置对应标签
results = (pd.Series(draws)
           .groupby(bins)
           .agg(['count', 'min', 'max'])
           .reset_index()) #reset_index()#默认drop=False  获得新的index，原来的index变成数据列保留下来  (drop=True)不保留原来的index
print(results)
print(results['quartile'])

#练习2
N = 10000000
draws = pd.Series(np.random.randn(N))
labels = pd.Series(['foo', 'bar', 'baz', 'qux'] * (N // 4))
categories = labels.astype('category')  #转化category 类型
print(labels.memory_usage())  #查看储存量大小
categories.memory_usage()   #查看储存量大小    category 类型  储存量小

# transform是与groupby（pandas中最有用的操作之一）组合使用的。一般情况下，我们在groupby之后使用aggregate , filter 或 apply来汇总数据，transform 会把算出的值回传到原来位置

