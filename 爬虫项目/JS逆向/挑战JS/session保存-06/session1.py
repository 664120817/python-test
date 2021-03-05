import requests
session =requests.session()

url="http://www.python-spider.com/api/challenge6"
headers={

"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Content-Length":"6",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Host":"www.python-spider.com",
"Origin":"http://www.python-spider.com",
"Pragma":"no-cache",
"Referer":"http://www.python-spider.com/challenge/4",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
"X-Requested-With":"XMLHttpRequest",

}
total=0
for page in range(1,101):
    for j in range(1, 9):
        print("第:" + str(page) + "页\n")
        data = {
            "page": page,
        }
        response =session.post(url,data=data)
        # print(response.text)
        if response.status_code != 200:
            continue
        arrays = response.json()['data']
        print(arrays)
        for item in arrays:
            num = item['value']
            total = total + int(num)
        print("total:",total)
        break

print("total: " + str(total))