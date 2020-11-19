import requests
import execjs


user = ""
pwd =""

def get_pwd():
    with open("./js/sk.js") as f:
       js_code = f.read()
       results = execjs.compile(js_code).call("test",pwd)
       return results

def login():

    url ="http://login.shikee.com/check/?"
    headers={
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "login.shikee.com",
        "Origin": "http://login.shikee.com",
        "Referer": "http://login.shikee.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    data ={

        "username": user,
        "password": get_pwd(),
        "vcode": "",
        "to": "http://lodin.shikee.com/",

    }

    session = requests.session()
    response = session.post(url=url, data=data, headers=headers)
    print(response.text)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "referer": "https://login.yizhanhulian.com/login",
    }
    url1="http://login.shikee.com/success/?to=http%3A%2F%2Fwww.shikee.com%2F"
    response = session.get(url=url1,headers=headers)
    print(response.text)

login()