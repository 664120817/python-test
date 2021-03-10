import requests,json
import execjs

def get_safe():
    with open("2.js") as f:
       js_code = f.read()
       safe = execjs.compile(js_code).call("test")
       print(safe)
       return safe

url="http://www.python-spider.com/api/challenge16"

headers ={

"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Content-Length":"6",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Cookie":"__jsl_clearance=1614946683.347|0|clD4VpfqhdaLBWywKWy%2FZyfi6d_d04c395d758bc21b37dd9cadea5d78973D; Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1615001120,1615097413,1615178890,1615267254; no-alert=true; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1615282209",
"Host":"www.python-spider.com",
"Origin":"http://www.python-spider.com",
"Pragma":"no-cache",
"Proxy-Connection":"keep-alive",
"Referer":"http://www.python-spider.com/challenge/16",
"safe":get_safe(),
# "safe":"MTYxNTMwNDA1MA==|AAAAAAAAAUAAAAAAAAAAAAAAAMAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAgAAAAAAAAABAAAAAAAAAAAAAAACAAAAAAAAAAGAAAAAAAAAAAAAAADAAAAAAAAAAUAAAAJAAAAAAAAAAUAAAABAAAAAgAAAAUAAAADAAAABQAAAAAAAAACAAAABwAAAAAAAAAJAAAAAQAAAAAAAAAGAAAAAA1d3ujLFy1k1d3HCsEByds52TQ6w",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
"X-Requested-With":"XMLHttpRequest",

}

total =0
for page in range(1,101):
    for j in range(1, 9):
        print("第:" + str(page) + "页\n")
        data = {
            "page": page,
        }

        response =requests.post(url=url,data=data,headers=headers)
        response1 =response.text
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