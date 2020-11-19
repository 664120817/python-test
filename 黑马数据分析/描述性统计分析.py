import numpy as np
import pandas as pd
from scipy import stats
import os
os.chdir(r'C:\Users\Administrator\Desktop\数据')
f = open(r"宝马3.csv")
BOM=pd.read_csv(f,usecols=['名字','公里','售价'],dtype={'公里':'str'})
print(BOM)
BOM.dropna(subset=['名字','公里','售价'],inplace=True,axis=0)
print(BOM)
BOM['公里']=BOM['公里'].astype(float)
print('统计中位数:',BOM['公里'].median())
print('统计分位数:',BOM['公里'].quantile([0,0.25,0.5,0.75]))
print('重数(出现频率最多的):',BOM['公里'].mode())  #重数可能有多个
print('分类变量:',BOM['公里'].value_counts())
print('极差:',BOM['公里'].max()-BOM['公里'].min())
print('变异系数:',BOM['公里'].std()/BOM['公里'].mean())
se=stats.sem(BOM['公里'])
print('计算样本标准:',se)
print("95%的区间范围",stats.norm.interval(0.95, BOM['公里'].mean(), se))
#pearson皮尔森相关性系数   spearman斯皮尔曼 相关分析  参考：https://www.cnblogs.com/yjd_hycf_space/p/11537153.html     比较常见相关系数分析
# data.corr(method="pearson")#皮尔森相关性系数 X1.corr(Y1,method="pearson")
# data.corr(method='spearman') spearman斯皮尔曼 r=x1.corr(y1,method='spearman')
""" 
#pearson皮尔森相关性系数   spearman斯皮尔曼 相关分析  参考：https://www.cnblogs.com/yjd_hycf_space/p/11537153.html     比较常见相关系数分析
#假设检验 参考：https://blog.csdn.net/lzx159951/article/details/104432582?
#卡方分析和方差分析  参考：https://blog.csdn.net/lzx159951/article/details/104435561
import pandas as pd
from scipy import stats
titanic = pd.read_csv('titanic.csv')
print(titanic.head(10))
table1 = pd.crosstab(titanic['pclass'],titanic['survived'],margins=False)#交叉表，用于统计两个变量之间的数据个数。
result = stats.chi2_contingency(table1)#卡方检验函数
print(result)
#不同等级舱与是否存活是由显著差异的

import pandas as pd
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
tips = pd.read_csv('tips.csv')
print(tips.head(10))
model = ols('tip ~ C(sex)+C(day)+C(time)',data=tips).fit()#用来配置几个相关联的变量
result = anova_lm(model)#方差分析函数
print(result)


"""
