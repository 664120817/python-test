import requests,time,re,urllib
import execjs
session = requests.session()

user = ""
pwd =""


def get_pwd(pwd,user):
    with open("./js/189.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test",pwd)
       users = execjs.compile(js_code).call("test", user)
       return pwds, users
def get_yzm():
    HEADEAS = {

        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "open.e.189.cn",
        "Referer": "https://open.e.189.cn/api/logbox/oauth2/unifyAccountLogin.do?appId=189mail&version=v1.0&clientType=10010&paras=9C865333E4D631BDE2820444F94D176A440DFD63AA8CEE61501CF1F35ED61E7F6613DB4FB0B89ED97C767997D3B29EC580B9BF52E48C407287C21F199D022CD91A97E02287999E6AD74D9CC8F66C1B4E9AE87F7835F7CC729134C8DF78F599B9254F15B15CDFE519827709A105160CA4B999FB7D6E9A67E243DB16342BCC899925639B785904FBF62F67D98984386685664166D8E5128775246435C152DBDE3475C15F619DC1C140AB55128608C2D8E2&sign=C3ADD26D4627488499E4628A2B652A9FC70BB602&format=redirect",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }

    date =round(int(time.time()*1000))
    print(date)
    url= "https://open.e.189.cn/api/logbox/oauth2/picCaptcha.do?"
    parms ={
        "Htoken": "bc4927d26253f26af48768aa88ed2955k88qtac0",
        "REQID": "e234ae1b67ba44a1",
        "rnd": date,
    }
    imge = session.get(url=url,params=parms, headers=HEADEAS)
    print(imge)
    with open("yzm_189邮箱.jpg", "wb") as f:
        f.write(imge.content)
# get_yzm()
def login():
    pwds, users = get_pwd(pwd,user)
    url ="https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
    headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Host": "open.e.189.cn",
        "lt": "8293C24EB9430FC1595F33F048ACDDE74AA7689C9EF57232FEEED6E84A4584FA386B641ABDDC8E4292B96E5F1ED8022D03679F720EACADA5A723484C82203AAF890890C2750DB423967ECCF2FE443CC42D394C8750380C2E",
        "Origin": "https://open.e.189.cn",
        "Referer": "https://open.e.189.cn/api/logbox/oauth2/unifyAccountLogin.do?appId=189mail&version=v1.0&clientType=10010&paras=9C865333E4D631BDE2820444F94D176A440DFD63AA8CEE61501CF1F35ED61E7F6613DB4FB0B89ED97C767997D3B29EC580B9BF52E48C407287C21F199D022CD91A97E02287999E6AD74D9CC8F66C1B4E9AE87F7835F7CC729134C8DF78F599B9254F15B15CDFE519827709A105160CA4B999FB7D6E9A67E243DB16342BCC899925639B785904FBF62F67D98984386685664166D8E5128775246435C152DBDE3475C15F619DC1C140AB55128608C2D8E2&sign=C3ADD26D4627488499E4628A2B652A9FC70BB602&format=redirect",
        "REQID": "e234ae1b67ba44a1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",

    }

    data ={
        "appKey": "189mail",
        "accountType": "01",
        "userName": users,
        "password": pwds,
        "validateCode": "t8hd",
        "captchaToken": "bc4927d26253f26af48768aa88ed2955k88qtac0",
        "returnUrl": "https://webmail30.189.cn/w2/logon/unifyPlatformLogonReturn.do",
        "mailSuffix": "@189.cn",
        "dynamicCheck": "FALSE",
        "clientType": "10010",
        "cb_SaveName": "0",
        "isOauth2": "false",
        "state": "",
        "paramId": "FA3FBDCC0B783A7E67D6285C0A1155F79F71CB1580118053FE119CA799865E137941EC25C578F8E2",

    }

    response = session.post(url=url, data=data, headers=headers)

    print(response.text)

login()