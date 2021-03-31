import requests,execjs,time,re

print(round(time.time()*1000))

headers = {
    "Referer": "https://passport.kongzhong.com/login?backurl=http://www.kongzhong.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",

}
dc_url= "https://sso.kongzhong.com/ajaxLogin?j=j&jsonp=j&service=https://passport.kongzhong.com/&_="+str(round(time.time()*1000))


response=requests.get(dc_url,headers=headers).text
print(response)
dc =re.findall(r'{"dc":(.*?),"kzmsg"',response)[0]
print(dc)
pwd="123456"
def get_pwd(pwd,dc):
    with open("./js/kzw.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test",pwd,dc)
       print("pwds:",pwds)
       return pwds

def get_yzm():

    url= "https://sso.kongzhong.com/createVCode"

    imge = requests.get(url=url, headers=headers)
    print(imge)
    with open("kzw.jpg", "wb") as f:
        f.write(imge.content)

yzm = get_yzm()



login_url="https://sso.kongzhong.com/ajaxLogin?j=j&"

params={
# "j":"j",
"type":"1",
"service":"https://passport.kongzhong.com/",
"username":"664120817",

"password":get_pwd(pwd,dc),
"vcode":input("输入验证码"),
"toSave":"0",
"_":round(time.time()*1000),


}

response=requests.get(login_url,headers=headers,params=params)
print(response.url,response.text)