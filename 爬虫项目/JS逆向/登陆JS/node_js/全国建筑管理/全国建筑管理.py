import requests,execjs

def get_pwd(data):
    with open("./js/qgjz.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("h",data)
       print(pwds)
       return pwds


def login():
    url ="http://jzsc.mohurd.gov.cn/api/webApi/asite/qualapt/aptData"
    # url ="http://jzsc.mohurd.gov.cn/data/company"
    headers={
        "Content-Type": "pplication/x-www-form-urlencoded; charset=UTF-8",
        # "Referer": "ttps://mp.weixin.qq.com/",
        "User-Agent": "ozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "X-Requested-With": "MLHttpRequest",
    }


    response = requests.get(url = url,headers =headers)
    print(response)
    print(response.text,"8888888")
    get_pwd(response.text)

login()