import requests,re,base64
from fontTools.ttLib import TTFont
headers ={

"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9",
"cache-control":"max-age=0",
"cookie":"f=n; commontopbar_new_city_info=158%7C%E6%AD%A6%E6%B1%89%7Cwh; userid360_xml=1203DAE4FE57A4A7575FDF2C86756715; time_create=1595748509588; id58=c5/nfF6q6ytDi/SMCbifAg==; wmda_uuid=19e4cd771dcfa307c0a4927ff9841a54; wmda_new_uuid=1; 58tj_uuid=133c7fa6-d580-498e-9aad-90742f0301f8; xxzl_deviceid=2SjZ1sMR5Ef9pP6omjvLB%2BJ49%2F%2Fn33Z3gj7pElGvIRS6fh0v7%2B3BOSEF6UtlcGkE; als=0; Hm_lvt_dcee4f66df28844222ef0479976aabf1=1592806175; ppStore_fingerprint=23F5F8E4CF30A014A81E1130C3E6A34F73FC994C3E2F11F6%EF%BC%BF1592806174799; fang_user_common=b5644e437373437aa7b483bc6f9902f7; wmda_visited_projects=%3B11187958619315%3B10104579731767; myLat=""; myLon=""; mcity=wh; f=n; commontopbar_new_city_info=158%7C%E6%AD%A6%E6%B1%89%7Cwh; city=wh; 58home=wh; commontopbar_ipcity=wh%7C%E6%AD%A6%E6%B1%89%7C0; new_uv=2; xxzl_cid=266ad3360ac04e80ab58f4f8f5f79e31; xzuid=e2b2f260-3cf3-4203-a117-3184070a09c5",
"referer":"https://callback.58.com/antibot/verifycode?serialId=8e31a7ebc7c5cc8e8c3ffee140c74b64_97e36555e9be404d8c86caeee3c7a963&code=23&sign=1e21732be0c3480f126319c77d340e1d&namespace=zufanglistphp&url=https%3A%2F%2Fwh.58.com%2Fzufang%2F%3Fkey%3D%25E7%25A7%259F%25E6%2588%25BF%25E5%25AD%2590%26cmcskey%3D%25E7%25A7%259F%25E6%2588%25BF%25E5%25AD%2590%26final%3D1%26jump%3D1%26sourcetype%3D11%26utm_source%3Dmarket%26spm%3Du-2d2yxv86y3v43nkddh1.BDPCPZ_BT%26PGTID%3D0d100000-0009-e9a4-57ff-de16c8e8b2b2%26ClickID%3D2",
"upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",

}
url ="https://wh.58.com/zufang/?key=%E7%A7%9F%E6%88%BF%E5%AD%90&cmcskey=%E7%A7%9F%E6%88%BF%E5%AD%90&final=1&jump=1&sourcetype=11&utm_source=market&spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT&PGTID=0d100000-0009-e9a4-57ff-de16c8e8b2b2&ClickID=2"
response =requests.get(url=url,headers=headers).text
# print(response)
result =re.findall(r"base64,(.*?)\)",response,flags=re.S)[0]
print(result)
b =base64.b64decode(result)  #解码
# print(b)
with open("ztku01.woff","wb")as f:    #将解密的字体写入到字体文件中
    f.write(b)

fonts =TTFont("ztku01.woff") #读取字体文件
fonts.saveXML("ztku01.xml") #保存成XML文件

#读取字体文件
ttfont =TTFont('ztku01.woff')
#读取映射 网页中的加密的字符串到num_x
best_cmap =ttfont['cmap'].getBestCmap()
print(best_cmap)

new_best_cmap = {}
for key, value in best_cmap.items():  # 字典序列解包
    # print(key,value)
    num =  int(value[-1])
    if  num == 0:
        num =10
    # print(hex(key),value) #hex 将数字转成十六进制
    new_best_cmap.update({hex(key).replace("0","&#",1)+";":num-1})
    # new_best_cmap[hex(key)]=value
print(new_best_cmap)

for key, value in new_best_cmap.items():
    if key in response:
        response = response.replace(key, str(value))
print(response)