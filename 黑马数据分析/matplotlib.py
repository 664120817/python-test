# from numpy import *
# import pandas as pd
# a=array([1,2,4,5,6])
# b=tile(a,(6,1))
# print(b)
# print(b.shape)
#
# m=pd.read_html("https://baike.baidu.com/item/%E7%A7%92%E6%87%82%E6%98%9F%E8%AF%BE%E5%A0%82")
# print(m)
import numpy as np
import matplotlib.pyplot as plt
# plt.figure(figsize=(10,10),dpi=100)
# plt.axis([0,10,0,7]) #设置坐标轴长 先行后列
# plt.plot([1,0,9],[4,5,6],marker='o',markersize=0.2) # marker='o'画什么线 ,markersize=0.2 线的粗细
# # plt.savefig("折线图.png"，dpi=100，facecolor='green') #dpi=100 设置保存分辨率 facecolor='green'设置保存背景
# # plt.axis('off') #关掉坐标轴 不显示坐标轴
# plt.show()
#
# # 画出某城市一天温度变化折线图，温度范围28,-37度
# import random
# x1=range(24)
# x = [x for x in x1]
# y= [int(random.uniform(28,37)) for i in x1]
# y2=[int(random.uniform(1,12)) for i in x1]
# print(x,y)
# plt.figure(figsize=(10,5),dpi=80)
# plt.plot(x,y,label="gz")
# plt.plot(x,y2,color='r',linestyle='--',label="bj")#color 改变线条颜色 linestyle 线条风格
# #显示图例
# plt.legend(loc="lower left")
# #解决中文无法显示 报错 1，安装字体 删除缓存 配置文件
# from matplotlib import font_manager
# my_font = font_manager.FontProperties(fname="title_font.ttf")
# x_label_show = ["{}时".format(i) for i in x1]
# plt.xticks(x[::2],x_label_show[::2],fontproperties=my_font)#刻度，单位标签，字体
# plt.yticks(range(15,40,3))
# # 添加网格显示
# plt.grid(True,linestyle="--",alpha=0.5) #linestyle 线条风格  ,alpha 透明度
# plt.xlabel("时间",fontproperties=my_font)
# plt.ylabel("温度",fontproperties=my_font)
# plt.title("温度图",fontproperties=my_font)
#
# # plt.savefig("温度折线图.png")
# plt.show()

# #多个坐标系显示 -plt.subplots（面对象的画图方法）
# import random
# x1=range(24)
# x = [x for x in x1]
# y= [int(random.uniform(28,37)) for i in x1]
# y2=[int(random.uniform(1,12)) for i in x1]
# print(x,y)
# # plt.figure(figsize=(10,5),dpi=80)
# gigure,axes = plt.subplots(nrows=1,ncols=2,figsize=(20,15),dpi=100) #创建多个axes绘图区 nrows=行,ncols=列
# axes[0].plot(x,y,label="gz")
# axes[1].plot(x,y2,color='r',linestyle='--',label="bj")#color 改变线条颜色 linestyle 线条风格
# #显示图例
# # plt.legend(loc="lower left")
# axes[0].legend()
# axes[1].legend()
# #解决中文无法显示 报错 1，安装字体 删除缓存 配置文件
# from matplotlib import font_manager
# my_font = font_manager.FontProperties(fname="title_font.ttf")
# x_label_show = ["{}时".format(i) for i in x1]
# axes[0].set_xticks(x[::2])
# axes[0].set_xticklabels(x_label_show[::2],fontproperties=my_font)
# axes[0].set_yticks(range(15,40,3))
# axes[1].set_xticks(x[::2])
# axes[1].set_xticklabels(x_label_show[::2],fontproperties=my_font)
# axes[1].set_yticks(range(15,40,3))
# # 添加网格显示
# axes[0].grid(True,linestyle="--",alpha=0.5) #linestyle 线条风格  ,alpha 透明度
# axes[1].grid(True,linestyle="--",alpha=0.5) #linestyle 线条风格  ,alpha 透明度
# #添加描述信息
# axes[0].set_xlabel("时间",fontproperties=my_font)
# axes[0].set_ylabel("温度",fontproperties=my_font)
# axes[0].set_title("温度图",fontproperties=my_font)
# axes[1].set_xlabel("时间",fontproperties=my_font)
# axes[1].set_ylabel("温度",fontproperties=my_font)
# axes[1].set_title("温度图",fontproperties=my_font)
# # plt.savefig("温度折线图.png")    # props ={   'title':"标题",  'xlale':"标签"}      axes[i，j].set(**props) #以字典的方式来设置
# plt.show()

# # 随机自动绘多个图形
# fig, axes = plt.subplots(2, 2, sharex=True, sharey=True) # sharex=True, sharey=True  代表所有X,Y轴一样的比例
# for i in range(2):
#     for j in range(2):
#         axes[i, j].hist(np.random.randn(500), bins=50, color='k', alpha=0.5)
# plt.subplots_adjust(wspace=0, hspace=0)

# #绘制数学函数图像
# import numpy as np
# x=np.linspace(-10,10,1000) #linspace 随机 生成 -10到10 中1000个数
# y=2*x*x
# plt.figure(figsize=(10,5),dpi=80)
# plt.plot(x,y)
# plt.show()
#
# #散点图
# x=[1,25,24,23,45,55,24,15,16,25,26,44,3,42,1,22,43]
# y=[22,14,12,14,16,88,55,66,45,25,28,35,59,14,48,6,12]
# plt.figure(figsize=(10,5),dpi=80)
# plt.scatter(x,y，color='r') #color=np.random.random(3000).reshape((1000,3)) #随机生成颜色
# plt.show()

#柱状图
movie_names=['雷神','诸神','联盟','东方','寻梦','风暴']
tickets=[55,66,88,77,44,58]
plt.figure(figsize=(15,10),dpi=100)
x_ticks=range(len(movie_names))
plt.bar(x_ticks,tickets,width=0.5,color=['b','r','g','y','c'])  #随机生成颜色color=np.random.random(30).reshape((5,6))
#修改x刻度
plt.xticks(x_ticks,movie_names,) #set_xticklabels 设置刻度标签
# plt.xticks(np.linspace(0,100,5),list('ABCDE')) #把0-100x坐标分成 5份，坐标刻为ABCDE
plt.show()
#柱状图对比
movie_names=['雷神','诸神','联盟','东方']
first_day = [10587,10062,1275,1111]
first_weekend =[36645,36632,27964,34212]
plt.figure(figsize=(15,10),dpi=100)
plt.bar(range(len(movie_names)),first_day,width=0.2,label="first_day")
plt.bar([x+0.2 for x in range(len(movie_names))],first_weekend,width=0.2,label="first_weekend")
# plt.bar(range(len(movie_names)),first_weekend,width=0.2,label="first_weekend",bottom=first_day) bottom 堆叠在first_day上
plt.xticks([x+0.1 for x in range(len(movie_names))],movie_names,rotation =45) #rotation =45 让坐标旋转45°
plt.legend() #显示图例
plt.show()

# #直方图绘制
# import pandas as pds
# data=pds.read_excel(r"C:\Users\Administrator\Desktop\数据\武汉.xlsx")
# data1=data["人均"]
# data2=data.T
# data3 =data2.values[2]
# plt.figure(figsize=(15,10),dpi=88)
# distance =20 #组距
# group_num =int((max(data3)-min(data3))/distance) #组数
# plt.hist(data3,bins=group_num)
# # plt.hist(data3,bins=group_num,density=True) #y轴 以频率显示
# #修改x刻度
# plt.xticks(range(min(data3),max(data3)+distance,distance))
# plt.show()

# #饼图绘制
# movie_names=['雷神','诸神','联盟','东方','寻梦','风暴']
# tickets=[55,66,88,77,44,58]
# plt.figure(figsize=(15,10),dpi=100)
# plt.pie(tickets,labels=movie_names,colors=['b','r','g','y','c','k'],autopct="%1.2f%%") #autopct="%1.2f%%"显示百分比
# plt.axis('equal') #让显示的饼图保持圆形，
# #显示图例
# plt.legend()
# plt.show()

#读取图片
girl=plt.imread('girl.jpeg')
# girl=girl[::-1,::-1,::-1] #长 宽 颜色 都颠倒
girl1=girl[::5,::5] #每隔5个去一个数据
# print(girl,type(girl))
# print(girl.shape) #2维图片转化3维数组，分别代表 长 宽 颜色
# girl_split=np.split(girl,(100,300))[1]
# plt.imshow(girl_split)
# plt.imshow(girl)
plt.show()

#图片灰度化处理
#以平均值 灰化
im_data=girl.mean(axis=-1)
print(im_data.shape)
plt.imshow(im_data,cmap='gray')
plt.show()
#以红绿蓝权重比例 灰化 最符合人眼
a=np.array([0.299,0.587,0.114])
im_data1=np.dot(girl,a) #矩阵相乘 red*0.299+green*0.587 + blue*0.114
print(im_data1.shape)
plt.imshow(im_data,cmap='gray')
plt.show()

#3D绘图(自学)
from mpl_toolkits.mplot3d.axes3d import Axes3D
x=np.linspace(0,7,50)
y=np.linspace(-np.pi,np.pi)
X,Y=np.meshgrid(x,y)
def mk_Z(x,y):
    return 3+0.5*np.sin(X)*np.cos(Y)-np.cos(2-X)
Z=mk_Z(x,y)
axes=plt.subplot(121,projection = '3d')
# axes.plot_surface(X,Y,Z)
s=axes.plot_surface(X,Y,Z,rstride=50,cmap='rainbow')
plt.colorbar(s,shrink = 0.5)
plt.show()

#玫瑰图(自学)
#创建坐标图形
def show_rose(values,title):
    #玫瑰花瓣个数
    n=8
    angle = np.arange(0,2*np.pi,2*np.pi/n)
    #绘制的数据values
    radius = np.array(values)
    plt.axes([0,0,1,1],polar=True) #axis:(x,y轴) axes:(整个画面) [0,0,2,2] 将图形放大一倍 polar=False 为条形图
    color = np.random.random(size=24).reshape((8,3))
    plt.bar(angle,radius,color=color)
    plt.title(title,loc='left')
    plt.show()
v = [1,2,3,2,5,6,5,8]
show_rose(v,'test')


# 制图（多图绘制）千峰添加
plt.figure(figsize=(10,5),dpi=80)
plt1=plt.subplot(2,2,1)#(行，列，当前区域)
x1=[1,2,3,4,5]
y1=[5,3,5,23,5]
plt1.grid(color='r',linestyle='--',linewidth=2) #设置网格
line,=plt.plot(x1,y1)
# plt1.set_title("sin") #set_facecolor 设置背景颜色
# plt1.set_linewidth(5)
#另一种方法
plt.setp(line,linestyle='--',linewidth=3,marker='o')
plt.subplot(2,2,2)
x2=[5,2,3,8,6]
y2=[7,9,1,2,3]
plt.plot(x2,y2)
plt.subplot(2,1,2) #plt.subplot2grid((2,1),(1,1),colspan=2,rowspan=1)
x3=[5,7,12,15,2,14]
y3=[6,5,4,1,11,5]
plt.plot(x3,y3)
# plt.show()
#图形内添加文字
x=np.arange(0,2*np.pi,0.01)
plt.plot(np.sin(x))
plt.text(200,0,'sin(0)=0') #文本移到200，0
plt.annotate(s ='这是余弦',xy=(150,1),xytext=(200,1.01),arrowprops={'width':10,'headwidth':20,'headlength':10,'shrink':0.1}) #箭头指示说明
plt.show()