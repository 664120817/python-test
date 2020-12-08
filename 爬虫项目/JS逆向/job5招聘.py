import requests,time,re,urllib
import execjs
session = requests.session()

user = ""
pwd =""

HEADEAS = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
def get_pwd(pwd):
    with open("./js/zzp.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test",pwd)
       print(pwds)
       return pwds

def get_yzm():
    t=int(time.time()*1000)
    url = "http://zp.job5156.com/vcode/show/byUvCookie?"+ str(t)
    imge = requests.get(url, headers=HEADEAS)
    with open("jobyzm.png","wb") as f:
        f.write(imge.content)


def login(pwd):
    get_yzm()
    yzm=input("请输入验证码")
    pwds = get_pwd(pwd)
    url ="http://zp.job5156.com/login/com/zp/post"
    headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Host": "zp.job5156.com",
        "Origin": "http://zp.job5156.com",
        "Referer": "http://zp.job5156.com/login/com?errmsg=%E6%82%A8%E8%BE%93%E5%85%A5%E7%9A%84%E9%AA%8C%E8%AF%81%E7%A0%81%E9%94%99%E8%AF%AF%E3%80%82",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",

    }

    data = {

        "csrfKey": "d32a586c912d4dabe0ffd419b70b9a0c",
        "ref": "",
        "username": user,
        "password": pwds,
        "captcha": yzm,
        "keepLogin": "",

    }

    response = session.post(url=url, data=data, headers=headers)

    print(response.text)


login(pwd)