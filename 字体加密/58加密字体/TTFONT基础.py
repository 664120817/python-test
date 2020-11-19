from fontTools.ttLib import TTFont

base_font = TTFont('32927eec.woff')    	# 打开文件
base_font.saveXML('32927eec.xml')		# 将字体文件保存为xml文件
base_font.getBestCmap()				# 映射关系unicode跟Name
uni_list = base_font.getGlyphOrder()  #获取新字体文件的uni编码的坐标
print(uni_list)
best_cmap =base_font['cmap'].getBestCmap()
print(best_cmap,len(best_cmap))
# b=list(base_font['glyf'][name].coordinates)	# 字形的轮廓信息(坐标数据)
# print(b)


def parse_font():
    """
    获取新字体文件的uni编码的坐标
    :return:
    """
    base_font = TTFont('32927eec.woff')
    uni_list = base_font.getGlyphOrder()[2:]
    print(uni_list)

    num_dict = {}
    for name in uni_list:
    	# 获取字体坐标 [(142, 151), (154, 89), (215, 35)......]
    	# 循环遍历  [142, 151, 154, 89, 215, 35.....]
        coordinate = (list(base_font['glyf'][name].coordinates))
        font_0 = [i for item in coordinate for i in item]
        print(font_0)

parse_font()
# knn-近邻算法实现：
# 这里只需要传入新字体文件的坐标数组即可返回坐标对应的数字。

# -*- coding: utf-8 -*-


"""knn算法实现传入新字体文件的坐标数组返回比对后的数字"""

import numpy as np
from font_dataset import dataset_	# 字体样本数据集


def handle_dataset():
    """
    :return: 返回训练样本集，以及对应的标签
    """
    # 值得注意的是，样本数据的长度和新字体坐标数组的长度必须一致！！
    # 所以这里也要用zeros生成长度为200的数组,r然后再做替换
    lables = list(data[0] for data in dataset_)
    dataset = list(data[1] for data in dataset_)
    returnmat = np.zeros((len(dataset), 200))
    index = 0
    for data in dataset:
        returnmat[index, :len(data)] = data
        index += 1
    return returnmat, lables


def classify_knn(new_array, dataset, lables, k):
    """
    :param new_array: 新实例
    :param dataset:   训练数据集
    :param lables:    训练集标签
    :param k:         最近的邻居数目
    :return:          返回算法处理后的结果
    """
    # np.shape是取数据有多少组，然后生成tile生成与训练数据组相同数量的数据
    # 然后取平方
    # np.sum(axis=1) 取行内值相加,然后开发，求出两点之间的距离
    datasetsize = dataset.shape[0]
    diffmat = np.tile(new_array, (datasetsize, 1)) - dataset
    sqrdiffmat = diffmat ** 2
    distance = sqrdiffmat.sum(axis=1) ** 0.5
    # np.argsort将数值从小到大排序输出索引
    # dict的get返回指定键的值，如果值不在字典中返回默认值。
    # 根据排序结果的索引值返回靠近的前k个标签
    sortdistance = distance.argsort()
    count = {}
    for i in range(k):
        volelable = lables[sortdistance[i]]
        count[volelable] = count.get(volelable, 0) + 1
    count_list = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return count_list[0][0]


def knn_num(inX):
    """
    :param inX: 传入新字体文件的坐标数组
    :return:    返回比对后的对象的数字
    """
    # returnMats 返回一个长度为200的用0填充的数组
    # 生成长度为200的数组，将returnMats前面替换为传入的字体坐标数组
    returnMats = np.zeros([200])
    returnMats[:len(inX)] = inX
    inX = returnMats
    dataset, lables = handle_dataset()
    result = classify_knn(inX, dataset, lables, 5)
    return (result)
