import plotly as py
import plotly.graph_objs as go
# 离线绘图
# trace0 = go.Scatter(
#     x=[1, 2, 3, 4],
#     y=[10, 15, 13, 17]
# )
# trace1 = go.Scatter(
#     x=[1, 2, 3, 4],
#     y=[16, 5, 11, 9]
# )
# data = [trace0, trace1]
#
# py.offline.iplot(data, filename = 'fth.html')

import plotly.express as px
import plotly

tips = px.data.tips()  # 用px里的示例数据  参考： https://www.jianshu.com/p/21f8bc2ff882
print(tips.head())

trace_tip = go.Scatter(x=tips.total_bill.tolist(),
                       y=tips.tip.tolist(),
                       mode='markers+text',
                       # mode决定图上出现点，线，text等的组合形式
                       name='trace_tip',
                       marker=dict(color=tips['size'].tolist(),  # 上色类别   tolist()将矩阵转化为列表
                                   colorscale='Viridis',  # 指定颜色
                                   showscale=True,
                                   size=[i * 10 for i in tips['size'].tolist()]),  # 点大小
                       # showlegend=True,
                       text=tips['sex'].tolist(),
                       textposition='bottom center',
                       textfont=dict(size=18, color='LightSeaGreen'))

# plotly.offline.plot(dict(data=[trace_tip]),filename='plot.html')
fig = go.Figure(data=[trace_tip])
# 如果在这个基础上接着画，那就[trace_tip1, trace_tip2...]
fig.show()