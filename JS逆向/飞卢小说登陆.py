import requests,re
import execjs
import time
session = requests.session()

user = ""
pwd =""

headers={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
def get_time():
    times = int(round(time.time()))
    return times

def get_pwd(times):
    with open("./js/fl.js") as f:
       js_code = f.read()
       imges_url=execjs.compile(js_code).call("getimgurl",user)
       results = execjs.compile(js_code).call("test",pwd,times)
       return  imges_url,results

def get_canshu():
    url="https://u.faloo.com/regist/login.aspx?backurl=https%3A%2F%2Fb.faloo.com%2F"
    response = session.get(url,headers=headers)
    name = re.findall(r"<input name='(\w{8})'",response.text)[0]
    value =re.findall(r'<input .* value="(\d{4})"',response.text)[0]
    return  name,value

def get_yzm(imges_url):
    imge = session.get(url=imges_url,headers=headers)
    with open("yzm.jpg","wb") as f:
        f.write(imge.content)


def login():
    times = get_time()
    name, value = get_canshu()
    imges_url, results_pwd =get_pwd(times)
    get_yzm(imges_url)
    yzm = input("请输入验证码")
    url ="https://u.faloo.com/regist/Login.aspx?"
    headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "u.faloo.com",
        "Referer": "https://u.faloo.com/regist/login.aspx?backurl=https%3A%2F%2Fb.faloo.com%2F",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    params ={

        "txtUserID": user,
        "txtPwd": results_pwd,
        "txtPwd4temp": "",
        "verifyCode": yzm,
        "ts": times,
        "t": "2",
        name: value,
        "backurl": "https://b.faloo.com/",

    }

    response = session.get(url=url, params=params, headers=headers)
    print(response.text)
    url="https://u.faloo.com"
    response = session.get(url=url, headers=headers)
    print(response.text)


login()

