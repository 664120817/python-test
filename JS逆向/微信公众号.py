import requests,time,re,urllib
import execjs
session = requests.session()

user = "1"
pwd =""

HEADEAS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "referer": "https://login.yizhanhulian.com/login",
    }

def get_pwd(pwd):
    with open("./js/wxgzh.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test",pwd)
       print(pwds)
       return pwds


def login(pwd):
    pwd =get_pwd(pwd)
    url ="https://mp.weixin.qq.com/cgi-bin/bizlogin?"
    headers={
        "Content-Type": "pplication/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "ttps://mp.weixin.qq.com/",
        "User-Agent": "ozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "X-Requested-With": "MLHttpRequest",
    }

    data = {
        "username": user,
        "pwd": pwd,
        "f":"json",
        # "imgcode": "xhxd",
        "redirect_url":"",
        "token":"",
        "userlang": "zh_CN",
        "lang": "zh_CN",
        "ajax": "1",
    }

    response = session.post(url = url,data = data,headers =headers)
    print(response)
    print(response.text,"8888888")


login(pwd)