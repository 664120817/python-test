import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
os.chdir(r'C:\Users\Administrator\Desktop\数据')

studay = pd.read_excel('学生.xls')
plt.figure(figsize=(12,10), dpi= 80)
print(studay)
# sns.set(style ='darkgrid',context='notebook',font_scale=1.2) #配置调色
# # plt.bar(studay.index.values,studay.gre,tick_label=studay.admit,color='steelblue')
# sns.barplot(x=studay.index,y='gre',data=studay,color='steelblue',orient='vertical')  #同上画图  更简便
# plt.ylabel("gre")
# plt.show()

# 官方API   http://seaborn.pydata.org/api.html     参考：https://www.cnblogs.com/abdm-989/p/12204640.html
"""常用的参数
* x,y,hue 数据集变量 变量名
* date 数据集 数据集名
* row,col 更多分类变量进行平铺显示 变量名
* col_wrap 每行的最高平铺数 整数
* estimator 在每个分类中进行矢量到标量的映射 矢量
* ci 置信区间 浮点数或None
* n_boot 计算置信区间时使用的引导迭代次数 整数
* units 采样单元的标识符，用于执行多级引导和重复测量设计 数据变量或向量数据
* order, hue_order 对应排序列表 字符串列表
* row_order, col_order 对应排序列表 字符串列表
* kind : 可选：point 默认, bar 柱形图, count 频次, box 箱体, violin 提琴, strip 散点，swarm 分散点
size 每个面的高度（英寸） 标量
aspect 纵横比 标量
orient 方向 "v"/"h"
color 颜色 matplotlib颜色
palette 调色板 seaborn颜色色板或字典
legend hue的信息面板 True/False
legend_out 是否扩展图形，并将信息框绘制在中心右边 True/False
share{x,y} 共享轴线 True/False"""
sns.barplot(x=studay.index,y='gre',hue='admit',data=studay,color='blue',palette='husl',orient='v') #palette='husl'  调色板  orient='v'画图指向
plt.ylabel("成绩")
plt.legend()
plt.show()