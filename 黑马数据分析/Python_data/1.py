#https://github.com/wesm/pydata-book    来自于此网站

import numpy as np
from numpy.linalg import inv,qr
import pandas as pd
X=np.random.randn(5,5)
mat = X.T.dot(X) #矩阵相乘
inv(mat) #逆矩阵

print(mat.dot(inv(mat)))
q,r =qr(mat) #np.linalg.qr() 计算矩阵的QR分解。把矩阵A作为QR，q是正交的，r是上三角形。

to_mach = pd.Series(['c','b','a','c','b','b','c','a'])
unique_vals =pd.Series(['c','b','a'])
print(to_mach.value_counts()) # 统计重复数量
print(pd.Index(unique_vals).get_indexer(to_mach)) #以不重复数 编号重复数字   #pd.Categorical.from_codes(codes, categories,ordered=True)    将codes=[0 1 2 0 1 1 0 2] categories=['c','b','a']  还原['c','b','a','c','b','b','c','a']

data = pd.DataFrame({'Q1':[1,3,4,3,4],'Q2':[2,3,1,2,3],'Q3':[1,5,2,4,4]})
print(data)  # transform是与groupby（pandas中最有用的操作之一）组合使用的。一般情况下，我们在groupby之后使用aggregate , filter 或 apply来汇总数据，transform 会把算出的值回传到原来位置
print(data.apply(pd.value_counts).fillna(0)) #以直方图格式显示数字出现的统计个数

# coun =pymysql.Connect(host="localhost", port=3306, user="root", passwd="4786874", db="spider", charset="utf8")
# Data = pd.read_sql('select jz1,jy1,jy3,jy6 from jjph',coun)
# Data=pd.DataFrame(Data,dtype=np.float).head(10)
# print(Data['jz1'].corr(Data['jy1']))
# print(Data.corr()) #求所以相关系数    Data.cov 协方差矩阵
# print(Data.corrwith(Data.jz1)) #与jz1的所有相关系数

#随机打散数据，防止数据偶然性
df = pd.DataFrame(np.arange(5 * 4).reshape((5, 4)))
sampler = np.random.permutation(5) #随机打散5的随机数
print(sampler)
print(df)
print(df.take(sampler))  #随机打散的数组
df.sample(n=3) #抓取任意打散的3行
choices = pd.Series([5, 7, -1, 6, 4])
draws = choices.sample(n=10, replace=True) #数子可被重复选取，n代表选取次数
print(draws)

#pandas里的正则

import re
text = "foo    bar\t baz  \tqux"
re.split('\s+', text)
regex = re.compile('\s+')
regex.split(text)
regex.findall(text)
text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com
"""
pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'

# re.IGNORECASE makes the regex case-insensitive
regex = re.compile(pattern, flags=re.IGNORECASE)
regex.findall(text)
m = regex.search(text)
print(m)
print(text[m.start():m.end()])
print(regex.match(text))
print(regex.sub('REDACTED', text))
pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex = re.compile(pattern, flags=re.IGNORECASE)
m = regex.match('wesm@bright.net')
m.groups()
regex.findall(text)
print(regex.sub(r'Username: \1, Domain: \2, Suffix: \3', text))
data = {'Dave': 'dave@google.com', 'Steve': 'steve@gmail.com',
        'Rob': 'rob@gmail.com', 'Wes': np.nan}
data = pd.Series(data)
print(data)
data.isnull()
data.str.contains('gmail')
print(pattern)
data.str.findall(pattern, flags=re.IGNORECASE)
matches = data.str.match(pattern, flags=re.IGNORECASE)
print(matches)
# matches.str.get(1)
# print(matches.str[0])
print(data.str[:5])
# pd.options.display.max_rows = PREVIOUS_MAX_ROWS