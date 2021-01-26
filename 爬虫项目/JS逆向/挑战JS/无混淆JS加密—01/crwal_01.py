import requests,time,base64,hashlib,json

timestamp =int(time.time())
print(timestamp)
a="9622"+str(timestamp)
b=base64.b64encode(a.encode())
print(b)
safe=hashlib.md5(b).hexdigest()
print(safe)
num=0
for page in range(1,86):
    url ="http://www.python-spider.com/challenge/api/json?page={}&count=14".format(str(page))
    print(url)
    headers={

    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    # "Cookie":"Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1610681214; sessionid=h18ea4c720bwlf7271y8j74ouba1c9lc; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1610681535",
    "Host":"www.python-spider.com",
    "Referer":"http://www.python-spider.com/challenge/1",
    "safe":safe,
    "timestamp":str(timestamp),
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",


    }

    res =requests.get(url=url,headers=headers).json()

    messages=[data['message'] for data in res['infos']]

    # print(messages)
    for message in messages:
        if "招" in message:
            print(message)
            num+=1
    time.sleep(0.2)
    print(num)