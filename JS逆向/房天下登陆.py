import requests
import execjs

sure =""
pwd =""

def get_pwd():
    with open("./js/sfw.js") as f:
       js_code = f.read()
       results = execjs.compile(js_code).call("test",pwd)
       return results

def login():

    url ="https://passport.fang.com/login.api"
    headers={
        "Content - Type": "application / x - www - form - urlencoded; charset = UTF - 8",
        "Host": "passport.fang.com",
        "Origin": "https://passport.fang.com",
        "Referer": "https://passport.fang.com/?backurl=https%3A%2F%2Fpassport.fang.com%2FRegister%2FRegisterSuccess%3Fphonenum%3D13349851825",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    data={
        "uid": sure,
        "pwd": get_pwd(),
         "Service": "soufun-passport-web",
        "AutoLogin": "1",

    }

    session = requests.session()
    response= session.post(url=url,data=data,headers=headers)
    print(response.text)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }
    url1="https://passport.fang.com/Register/RegisterSuccess?phonenum=13349851825"
    response= session.get(url=url1,headers=headers)
    print(response.text)


login()