from PIL import Image
from os import listdir #导入文件夹里所有文件的模块
import numpy

from numpy import *
import operator
def knn(k,testdata,traindata,labels):
    traindatasize=traindata.shape[0]
#tile(testdata,size)扩展列  tile(testdata,(size,1))扩展行
    dif=tile(testdata,(traindatasize,1))-traindata
    sqdif=dif**2
    sumsqdif=sqdif.sum(axis=1)#sqdif.sum(axis=0) 列相加 sqdif.sum(axis=1) 行相加
    distance=sumsqdif**0.5
    sortdistance=distance.argsort()
    count={}
    for i in range(0,k):
        vote=labels[sortdistance[i]]
        count[vote]=count.get(vote,0)+1
    sortcount=sorted(count.items(),key=operator.itemgetter(1),reverse=True)#降序排列
    return sortcount[0][0]


#图片处理 pillow
#先将所有图片转为固定高，比如32*32，在转为文本
im=Image.open(r"C:\Users\Administrator\Desktop\20170415074136494\图片\美女.jpg")
fh=open(r"C:\Users\Administrator\Desktop\20170415074136494\traindata\美女.txt","a")
width=im.size[0]
height=im.size[1]
print(width,height)
# k=im.getpixel((0,9))#像素颜色[0,0,0]白色
# print(k)

for i in range(0,width):
    for j in range(0,height):
        cl=im.getpixel((i,j))#获取对应像素
        clall=cl[0]+cl[1]+cl[2]#判断像素
        if (clall==0): #黑色
            fh.write("1")
        else:
            fh.write("0")
    fh.write("\n")
fh.close()


# #加载数据
# def datatoarry(fname):
#     arr=[]
#     fh=open(fname)
#     width = len(fh.readline())
#     print(width)
#     for i in range(0,width):
#         thisline=fh.readline()
#         for j in range(0,358):
#             thisline[j]
#             arr.append(int(thisline[j]))
#     # print(arr)
#     return arr
#
# # arr1=datatoarry(r"C:\Users\Administrator\Desktop\20170415074136494\traindata\蝴蝶.txt")
# #建立一个函数取文件名前缀
# def seplabel(fname):
#     filestr=fname.split(".")[0]
#     return filestr
# # 建立训练数据
# def traindate():
#     labels=[]
#     trainfile=listdir(r"C:\Users\Administrator\Desktop\20170415074136494\traindata")
#     num=len(trainfile)
#     #长度1024（列），每一行储存一个文件
#     #用一个数组储存所有训练数据，行：文件总数，列：1024
#     trainarr=numpy.zeros((num,161458))#生成NUM行，1024列的
#     for i in range(0,num):
#         thisfname=trainfile[i]
#         thislabel=seplabel(thisfname)
#         labels.append(thislabel)
#         trainarr[i,:]=datatoarry(r"C:\Users\Administrator\Desktop\20170415074136494\traindata/"+thisfname)
#     return trainarr,labels
#
# # 用测试数据调用KNN算法去测试，看是否能够准确识别
# def datatest():
#     trainarr, labels=traindate()
#     testlist=listdir(r"C:\Users\Administrator\Desktop\20170415074136494\traindata")
#     tnum=len(testlist)
#     for i in range(0,tnum):
#         thistestfile=testlist[i]
#         testarr=datatoarry(r"C:\Users\Administrator\Desktop\20170415074136494\traindata/"+thistestfile)
#         rknn=knn(1,testarr,trainarr,labels)
#         print(rknn)
# datatest()