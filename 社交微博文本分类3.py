#文本分类(情感分析)
#加载文本
#将文本转为特征矩阵（*）
#构建算法
#分好训练数据和测试数据
#对数据进行训练
#对数据进行预测（测试）
import numpy
import pandas
from sklearn.feature_extraction.text import CountVectorizer
vectorizer=CountVectorizer()
data=pandas.read_excel(r"C:\Users\Administrator\Desktop\爬虫\数据分析与挖掘\微博心情.xlsx",header=None,decode="utf-8")
weibo=data.values
num=len(weibo)
num1=int(num*0.2)
# tlabels=[]
# for i in range(num1):
#     print("第"+str(i)+"条微博为"+weibo[i])
#     thislabels=input("请输入微博情感类别：1正向,0中向,-1负向")
#     tlabels.append(thislabels)
# print(tlabels)
# 微博切词
import jieba
cutdata=[]
for i in range(0,num):
    thisdata=weibo[i][0]
    thiscut=jieba.cut(thisdata,cut_all=False)
    print(thiscut)
    thiscutdata=""
    for j in thiscut:
        print(j)
        thiscutdata=thiscutdata +j+" "
    cutdata.append(thiscutdata)
# print(cutdata)
x=vectorizer.fit_transform(cutdata)
alltz=x.toarray()#将文本转成矩阵
# print(alltz)
#获取训练数据矩阵
trainlabels=['1', '0', '1', '0', '1', '1', '1', '-1', '1', '-1', '-1', '0', '-1', '-1', '1', '1', '0', '1', '0', '1', '-1', '1', '1', '0', '-1', '0', '0', '0', '1', '-1', '1', '-1']
traindata=alltz[0:num1,:]
xf=pandas.DataFrame(traindata)
yf=pandas.DataFrame(trainlabels)
print(yf)
trainarr=xf.values.astype(int)
trainlabels=yf.values.T[0].astype(int)
print(traindata,trainlabels)
#测试数据
testdata=alltz[num1:,:]
print(testdata)
#构建模型(KNN,贝叶斯,人工神经网络)
from keras.models import Sequential
from keras.layers.core import Dense,Activation
model=Sequential()
#输入层
model.add(Dense(10,input_dim=len(traindata[0])))#(输入层，特征)
model.add(Activation("relu"))
#输出层
model.add(Dense(1,input_dim=1))
model.add(Activation("sigmoid"))
#模型的编译
model.compile(loss="mean_squared_error",optimizer="adam",metrics=['accuracy'])#（二元损失函数，求解法方，模式）
#训练
model.fit(traindata,trainlabels,epochs=100,batch_size=100)#（学习次数，）
#预测分类
rst=model.predict_classes(testdata).reshape(len(testdata))#预测x下的y值，reshap改变维数
print(rst,len(testdata))


