import requests
import execjs

user = ""
pwd =""

def get_pwd():
    with open("./js/ccj.js") as f:
       js_code = f.read()
       results = execjs.compile(js_code).call("test",pwd)
       return results

def login():

    url ="http://seller.chuchujie.com/sqe.php?s=/AccountSeller/login"
    headers={
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "seller.chuchujie.com",
        "Origin": "http://seller.chuchujie.com",
        "Referer": "http://seller.chuchujie.com/sqe.php?s=/User/index",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",}

    data ={

        "username":user,
        "password": get_pwd(),
        "login_type": "",
        "sms_code": "",
        "redirect_uri": "",
        "channle": "",
    }
    session=requests.session()
    response =session.post(url=url,data=data,headers=headers)
    print(response.text)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }
    url1="http://seller.chuchujie.com/sqe.php?s=/User/index"
    response = session.get(url=url1, headers=headers)
    print(response.text)


login()
