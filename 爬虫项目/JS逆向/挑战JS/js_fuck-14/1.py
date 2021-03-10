import requests,json,re,execjs
from lxml import etree
url="http://www.python-spider.com/api/challenge14"

headers={

"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Content-Length":"38",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Cookie":"__jsl_clearance=1614946683.347|0|clD4VpfqhdaLBWywKWy%2FZyfi6d_d04c395d758bc21b37dd9cadea5d78973D; Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1615097413,1615178890,1615267254,1615351495; no-alert=true; sessionid=ixlw76ckeng4q3i3d75l5bayscyuypau; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1615354761",
"Host":"www.python-spider.com",
"Origin":"http://www.python-spider.com",
"Pragma":"no-cache",
"Proxy-Connection":"keep-alive",
"Referer":"http://www.python-spider.com/challenge/14",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
"X-Requested-With":"XMLHttpRequest",

}
def get_uc(page):
    with open("fk.js") as f:
       js_code = f.read()
       safe = execjs.compile(js_code).call("call",page)
       print(safe)
       return safe

total =0
for page in range(1,101):
    for j in range(1, 9):
        print("第:" + str(page) + "页\n")
        data = {
            "page": page,
            "uc":get_uc(page)
        }
        print(data)

        response =requests.post(url=url,data=data,headers=headers)
        response1 =response.text
        print(response1)
        if response.status_code != 200:
            continue
        res = json.loads(response1)
        arrays = res['data']
        print(arrays)
        for item in arrays:
            num = item['value']
            print("num", num)
            total = total + int(num)
        print("total:", total)
        break

print("total: " + str(total))