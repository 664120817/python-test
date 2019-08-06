from PIL import Image
from os import listdir #导入文件夹里所有文件的模块

import numpy
class Bayes:
    def __init__(self):
        self.length=-1
        self.labelcount=dict()#标签
        self.vectorcount=dict()#向量
    def fit(self,dataSet:list,labels:list):#dataSet训练的数据集
        if(len(dataSet)!=len(labels)):
            raise ValueError("您输入的测试数组跟类别数组长度不一致")
        self.length=len(dataSet[0])#测试特征值的长度
        labelsnum=len(labels)#所有类别的数量
        norlabels=set(labels)#不重复类别的数量
        for item in norlabels:
            self.labelcount[item]=labels.count(item)/labelsnum#获取labels相同个数/总个数=所占比例 当前类别占总数比例
        for vector,label in zip(dataSet,labels):#整合在一起
            if(label not in self.vectorcount):
                self.vectorcount[label]=[]
            self.vectorcount[label].append(vector)
        print("训练结束")
        return self
    def btest(self,TestDate,labelsSet):
        if (self.length==-1):
            raise ValueError("您还没有进行训练，请先训练")
        #计算testdata分别为各个类别的概率
        IbDict=dict()
        for thisIb in labelsSet:
            p=1
            alllabel=self.labelcount[thisIb]
            allvector=self.vectorcount[thisIb]
            vnum=len(allvector)
            allvector=numpy.array(allvector).T
            for index in range(0,len(TestDate)):
                vector=list(allvector[index])
                p*=vector.count(TestDate[index])/vnum
            IbDict[thisIb]=p*alllabel
        thislabel=sorted(IbDict,key=lambda x:IbDict[x],reverse=True)[0]
        return thislabel

def datatoarry(fname):
    arr=[]
    fh=open(fname)
    width = len(fh.readline())
    # print(width)
    for i in range(0,width):
        thisline=fh.readline()
        for j in range(0,358):
            thisline[j]
            arr.append(int(thisline[j]))
    return arr
#建立一个函数取文件名前缀
def seplabel(fname):
    label=fname.split(".")[0]
    return label
# 建立训练数据
def traindate():
    labels=[]
    trainfile=listdir(r"C:\Users\Administrator\Desktop\1234\PyQt5_Demo\resource\images\训练")
    num=len(trainfile)
    #长度1024（列），每一行储存一个文件
    #用一个数组储存所有训练数据，行：文件总数，列：1024
    trainarr= numpy.zeros((num,128522))#生成NUM行，1024列的
    for i in range(0,num):
        thisfname=trainfile[i]
        thislabel=seplabel(thisfname)
        labels.append(thislabel)
        trainarr[i]=datatoarry(r"C:\Users\Administrator\Desktop\1234\PyQt5_Demo\resource\images\训练/"+thisfname)
    return trainarr,labels
bys=Bayes()
#训练数据
trainarr,labels=traindate()
bys.fit(trainarr,labels)
#测试 #识别单个字体
thisdata=datatoarry(r"C:\Users\Administrator\Desktop\1234\PyQt5_Demo\resource\images\训练\4.txt")
print(labels)
# labelsall=["0","1","2","3","4","5","6"]
rst=bys.btest(thisdata,labels)
print(rst)
#识别多个手写字体（批量测试）
testfileall=listdir(r"C:\Users\Administrator\Desktop\1234\PyQt5_Demo\resource\images\训练")
num=len(testfileall)
for i in range(0,num):
    thisfilename=testfileall[i]
    print(thisfilename)
    thislabel=seplabel(thisfilename)
    thisdataarray=datatoarry(r"C:\Users\Administrator\Desktop\1234\PyQt5_Demo\resource\images\训练/"+thisfilename)
    label=bys.btest(thisdataarray,labels)
    print("该数字是："+thislabel+",识别出来的数字是："+ label)
#错误率计算
    x=0
    if (label!=thislabel):
        x+=1
        print("此次出错")
print(x)
print("错误率是："+str(float(x)/float(num)))

