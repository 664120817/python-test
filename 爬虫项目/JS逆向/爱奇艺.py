import requests,time,re,urllib
import execjs
session = requests.session()

user = ""
pwd =""


def get_pwd(pwd):
    with open("./js/aqy.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test",pwd)
       print(pwds)
       return pwds



def login():
    pwds = get_pwd(pwd)
    url ="https://passport.iqiyi.com/apis/reglogin/login.action"
    headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Host": "passport.iqiyi.com",
        "Origin": "https://www.iqiyi.com",
        "Referer": "https://www.iqiyi.com/iframe/loginreg?ver=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",

    }

    data ={

        "email": "13349851825",
        "fromSDK": "1",
        "sdk_version": "1.0.0",
        "passwd": pwds,
        "agenttype": "1",
        "__NEW": "1",
        "checkExist": "1",
        "lang": "",
        "ptid": "01010021010000000000",
        "nr": "1",
        "verifyPhone": "1",
        "area_code": "86",
        "dfp": "a041c6ceb5ad274ceeb3e03bf6f092839dcb787872914bb49be3807e2777c76b7c",

    }

    response = session.post(url=url, data=data, headers=headers)

    print(response.text)

login()