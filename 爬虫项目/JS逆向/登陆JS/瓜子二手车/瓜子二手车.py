import requests,execjs,re
headers ={

"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Host":"www.guazi.com",
"Pragma":"no-cache",
"Referer":"https://www.guazi.com/wh/honda/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",

}
res=requests.get("https://www.guazi.com/wh/dazhong/o9/#bread",headers=headers)
# print(res.text)

value= re.findall(r"value=anti\((.*?)\);var name='",res.text)[0]
print("value:",value)
name='antipas'
url=''
def get_antipas(value):
    with open("2.js") as f:
       js_code = f.read()
       antipas = execjs.compile(js_code).call("anti",value)
       print("antipas:",antipas)
       return "antipas="+antipas

# get_antipas(value)
headers ={

"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
# "Cookie":get_antipas(value),
# "Cookie":"antipas=82vA8xl42052710W343Ia0;",
"Host":"www.guazi.com",
"Pragma":"no-cache",
"Referer":"https://www.guazi.com/wh/honda/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",

}


headers1={


"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9",
"Connection":"keep-alive",
"Cookie":get_antipas(value),
"Host":"www.guazi.com",
"Referer":"https://www.guazi.com/wh/buy/",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"same-origin",
"Sec-Fetch-User":"?1",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",





}
print(headers1)
res=requests.get("https://www.guazi.com/wh/dazhong/o1/#bread",headers=headers)
print(res.text)
