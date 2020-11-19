"""
用来将字体文件转换为可以读的模式
"""
from fontTools.ttLib import TTFont
import requests
# #读取字体文件
# ttfont =TTFont('iconfont_9eb9a50.woff')
# #保存成xml文件 变成可读的 xml文件专门用来保存数据的  传输数据    给人看对比找规律
# ttfont.saveXML('iconfont_9eb9a50.xml')
# 'http://fontstore.baidu.com/static/editor/index.html' #百度字体转化网址  首选百度转化

#读取字体文件
ttfont =TTFont('iconfont_9eb9a50.woff')
#读取映射 网页中的加密的字符串到num_x
best_cmap =ttfont['cmap'].getBestCmap()
# print(best_cmap)


def get_best_cmap():
    """

    :return: 返回映射表
    """
    new_best_cmap ={}
    for key,value in best_cmap.items():#字典序列解包
        # print(key,value)
        # print(hex(key),value) #hex 将数字转成十六进制
        new_best_cmap.update({hex(key):value})
        # new_best_cmap[hex(key)]=value
        # print(new_best_cmap)
    return new_best_cmap

def get_num_cmap():
    """
    #根据 http://fontstore.baidu.com/static/editor/index.html 获取对应数字
    :return: 返回num和真正数字的映射关系
    """
    num_cmap={
       'x':'','num_':'1','num_1':'0','num_2':'3','num_3':'2','num_4':'4',
        'num_5': '5','num_6':'6','num_7':'7','num_8':'8','num_9':'8',
    }
    return num_cmap

def map_cmap_num(get_best_cmap,get_num_cmap):
    """
    替换规律 'num_2':'3' 》》》Oxe604:3
    :param get_best_cmap:函数
    :param get_num_cmap:函数
    :return:返回值
    """
    result ={}
    for key,value in get_best_cmap().items():
        key=key.replace('0','&#',1) + ";"
        result[key] =get_num_cmap()[value]

    return result

def get_html(url):
    response= requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}).text
    return response

def replace_num_and_cmap(result,response):
    #替换文本数字
    for key,value in result.items():
        if key in response:
            response=response.replace(key,value)
    return response

def save_to_file(response):
    #保持网页
    with open('douyin.html',"w",encoding='utf-8') as f :
        f.write(response)

def get_data():
    #分析页面数据
    pass


if __name__ == "__main__":
    result=map_cmap_num(get_best_cmap,get_num_cmap)
    print(result)
    url='https://www.iesdouyin.com/share/user/104690340840'
    response=get_html(url)
    print(response)
    response=replace_num_and_cmap(result,response)
    html=save_to_file(response)