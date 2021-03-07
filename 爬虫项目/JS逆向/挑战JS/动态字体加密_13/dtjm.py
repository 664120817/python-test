import requests,json,re,execjs,base64
from fontTools.ttLib import TTFont


url="http://www.python-spider.com/api/challenge13"

headers={

"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Cookie":"sessionid=miryvak2y92990yb4s3iktuk83ix6m4s; sign=1612790744178~1ccdb96a1a5638a5aef2fc97050f65be; Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1612693138,1612707458,1612788514,1612790745; no-alert=true; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1612797627; __jsl_clearance=1612797642.648|0|clD4VpfqhdaLBWywKWy%2FZyfi6d_60fae300e2cf760413ef486f1354aa3d3D",
"Host":"www.python-spider.com",
"Pragma":"no-cache",
"Referer":"http://www.python-spider.com/challenge/11",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",


}

data = {
    "page": 1,
}

response = requests.post(url=url, data=data, headers=headers)
print(response.text)
total =0
for page in range(1,101):
    for j in range(1, 9):
        print("第:" + str(page) + "页\n")
        data = {
            "page": page,
        }

        response =requests.post(url=url,data=data,headers=headers)
        response1 =response.text
        # print(response.text,response.url)
        if response.status_code != 200:
            continue
        woff = response.json()['woff'].strip()
        data = response.json()['data']
        imgdata = base64.b64decode(woff)
        with open("./woff.woff", "wb") as f:
            f.write(imgdata)
        fonts = TTFont("woff.woff")  # 读取字体文件
        print("fonts:", fonts)
        fonts.saveXML("woff.xml")  # 保存成XML文件

        # 读取字体文件
        ttfont = TTFont('woff.woff')
        # 读取映射 网页中的加密的字符串到num_x
        best_cmap = ttfont['cmap'].getBestCmap()
        print("best_cmap:", best_cmap)

        best_extraNames = ttfont['post'].extraNames
        print("extraNames:", best_extraNames)

        dic = {}
        for i in best_extraNames:
            dic[i] = len(dic) + 1
        print(dic)
        new_best_cmap = {}
        for key, value in best_cmap.items():  # 字典序列解包
            # print(key,value)
            # print(hex(key),value) #hex 将数字转成十六进制
            if dic[str(value)] ==10:
                dic[str(value)]=0
            new_best_cmap.update({hex(key).replace("0", "&#", 1): dic[str(value)]})
            # new_best_cmap[hex(key)]=value
        # print("new_best_cmap:",new_best_cmap)
        for key, value in new_best_cmap.items():
            if key in response1:
                response1 = response1.replace(key + " ", str(value))
        res = json.loads(response1)
        arrays = res['data']
        print(arrays)
        for item in arrays:
            num = item['value']
            print("num",num)
            total = total + int(num)
        print("total:",total)
        break

print("total: " + str(total))