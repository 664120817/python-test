import requests,execjs,time

print(round(time.time()*1000))

headers = {
    "Accept":"*/*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Content-Length":"38",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"Cookie":"browserid=2491027438446005733; steamCountry=CN%7Cfbc91ee6dccaeea5548f06157e51181f; sessionid=2a3bdb4fbd8e8c9213d6df6f; timezoneOffset=28800,0; _ga=GA1.2.1803339031.1617086188; _gid=GA1.2.1035694084.1617086188; app_impressions=271590:771300@1_4_4__129_1|977950@1_4_4__129_2",
"Host":"store.steampowered.com",
"Origin":"https://store.steampowered.com",
"Pragma":"no-cache",
"Referer":"https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
"X-Requested-With":"XMLHttpRequest",

}
key_url= "https://store.steampowered.com/login/getrsakey/"
data={
"donotcache": round(time.time()*1000),
"username": "root"

}
response=requests.post(key_url,headers=headers,data=data).json()
# print(response)
publickey_mod=response["publickey_mod"]
publickey_exp=response['publickey_exp']
print(publickey_exp,publickey_mod)

pwd="123456"
def get_pwd(publickey_mod,publickey_exp,pwd):
    with open("./js/STEAM.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test",publickey_mod,publickey_exp,pwd)
       print("pwds:",pwds)
       return pwds




login_url= "https://store.steampowered.com/login/dologin/"
data={
"donotcache":round(time.time()*1000),
"password":get_pwd(publickey_mod,publickey_exp,pwd),
"username":"root",
"twofactorcode":"",
"emailauth":"",
"loginfriendlyname":"",
"captchagid":"-1",
"captcha_text":"",
"emailsteamid":"",
"rsatimestamp":"543785550000",
"remember_login":"false",

}
response=requests.post(login_url,headers=headers,data=data).text
print(response)

