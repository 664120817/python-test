import requests,time,base64,hashlib,json


# time_new = int(time.time())
# print(time_new)
time_new = 1587102734
token=base64.b64encode(("aiding_win"+str(time_new*1000)).encode("utf-8")).decode()
print(token)
ddd = base64.b64encode(("aiding_win"+str(time_new)).encode("utf-8"))
md =hashlib.md5(ddd).hexdigest()
ccc =str(time_new)+"~" + str(token) +"|"
cookie = ccc +md
print(cookie)

# 1587102734~YWlkaW5nX3dpbjE1ODcxMDI3MzQwMDA=|43ac417bd1f71a04c6b99835f9ee5fad


url ="http://www.python-spider.com/challenge/2"
headers={

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Cookie": "a[_$ob('0x55')](a[_$ob('0x55')](a[_$ob('0x39')](a[_$ob('0x39')](a['NqEaf'](a[_$ob('0x65')], Math[_$ob('0x68')](a[_$ob('0x19')](c, 0x3e8))), '~'), token), '|'), md), a[_$ob('0x3e')]undefined; Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1610681214; no-alert=true; sessionid=6np8onfp3q5o3jk2zxa5u9eh6q4iip5q; sign={}; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1610703389".format(cookie),
    "Host": "www.python-spider.com",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.python-spider.com/challenge/2",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",

}

res =requests.get(url=url,headers=headers).text
print(res)
