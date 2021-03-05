import requests,json


def get_porpy():
    try:
        response = requests.get('http://localhost:16888/random?protocol=http')
        if response.status_code == 200:
            ip = response.text
            print(ip)
            ips = {
                # "http":"http://117.191.11.110：8080",
                "http": ip
            }
            # response = requests.get(url="http://httpbin.org/ip", proxies=ips)
            response = requests.get(url="https://www.baidu.com/", proxies=ips)
            # print(response.text)
            if response.status_code == 200:
                return ip
            else:
               get_porpy()
    except Exception:
       get_porpy()

url="http://www.python-spider.com/api/challenge4"
headers={

"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Content-Length":"6",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Cookie":"Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1610862743,1610886374,1610934585,1612501862; sessionid=ez47cp11gm44qgoygbueq996cfe7f799; sign=1612501924~YWlkaW5nX3dpbjE2MTI1MDE5MjQzMTk=|cd88d09f7a4202f0197a69572ba0e76e; no-alert=true; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1612503002",
"Host":"www.python-spider.com",
"Origin":"http://www.python-spider.com",
"Pragma":"no-cache",
"Referer":"http://www.python-spider.com/challenge/4",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
"X-Requested-With":"XMLHttpRequest",


}
total = 0
for page in range(1,101):
    for j in range(1, 9):
        print("第:" + str(page) + "页\n")
        data={
        "page": page,
        }

        proxy = {
            "http": get_porpy(),
            # "https":"http://118.163.83.21:3128",
        }
        print(proxy)
        try:
           response =requests.post(url,data=data,headers=headers,proxies=proxy)
        except Exception:
            pass
        print(response.status_code)
        if response.status_code != 200:
            continue

        arrays = response.json()['data']
        print(arrays)
        for item in arrays:
            num = item['value']
            total = total + int(num)
            print(total)
        break

print("total: "+ str(total))