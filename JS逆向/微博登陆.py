import requests,time,re,urllib
import execjs
session = requests.session()

user = ""
pwd =""

HEADEAS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "referer": "https://login.yizhanhulian.com/login",
    }

def get_pwd(me):
    with open("./js/wb.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test",pwd,me)
       suers = execjs.compile(js_code).call("get_su", user)
       print(pwds,suers)
       return pwds,suers



def get_me():
    url ='https://login.sina.com.cn/sso/prelogin.php?'
    get_time = round(int(time.time() * 1000))
    params ={
        "entry": "weibo",
        "callback": "sinaSSOController.preloginCallBack",
        "su": "",
        "rsakt": "mod",
        "client": "ssologin.js(v1.4.19)",
        "_": get_time,
    }
    response =session.get(url=url,params=params,headers=HEADEAS).text
    me=eval(response.replace("sinaSSOController.preloginCallBack",""))
    print(me)
    return me





def login():
    me = get_me()
    print(me,"666")
    pwds,suers = get_pwd(me)
    print(me["nonce"],me["exectime"])
    get_time = round(int(time.time()))
    url ="https://login.sina.com.cn/sso/login.php?"
    headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"no-cache",
        "Connection":"keep-alive",
        "Content-Length":"828",
        "Content-Type":"application/x-www-form-urlencoded",
        "Host":"login.sina.com.cn",
        "Origin":"https://weibo.com",
        "Pragma":"no-cache",
        "Referer":"https://weibo.com/",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }

    data ={

        "entry": "weibo",
        "gateway": "1",
        "from": "",
        "savestate": "7",
        "qrcode_flag": "false",
        "useticket": "1",
        "pagerefer": "https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand=1584609416.9828",
        "vsnf": "1",
        "su": suers,
        "service": "miniblog",
        "servertime": get_time,
        "nonce": me["nonce"],
        "pwencode": "rsa2",
        "rsakv": me["rsakv"],
        "sp": pwds,
        "sr": "1920*1080",
        "encoding": "UTF-8",
        "prelt": me["exectime"],
        "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
        "returntype": "META",

    }

    response = session.post(url=url, data=data, headers=headers)
    text = response.content.decode("gb2312")
    text = (urllib.parse.unquote(text))
    print(text)

    url1 =re.findall(r'location.replace\("(.*?)"\);.*',text)[0]

    ticket = re.findall(r'ticket=(.*?)&retcode',text)[0]
    ssosavestate = re.findall(r'ssosavestate=(.*?)&url.*',text)[0]
    print(ticket,ssosavestate,"123456")
    headers = {
        "Host": "passport.weibo.com",
        "Pragma": "no-cache",
        "Referer": url1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",

    }

    url0 = "https://passport.weibo.com/wbsso/login"
    params={
        "ticket": ticket,
        "ssosavestate": ssosavestate,
        "callback": "sinaSSOController.feedBackUrlCallBack",
        "scriptId": "ssoscript0",
        "client": "ssologin.js(v1.4.19)",
        "_": get_time,

    }
    response = session.get(url=url0,params=params, headers=headers)
    print(response.content.decode("gbk"))

    response = session.get(url=url1, headers=HEADEAS)
    print(response.content.decode("gbk"))

    # url2 = "https://account.weibo.com/set/index?"
    url2 ="https://weibo.com/u/2156118037/home?leftnav=1"
    response = session.get(url=url2)
    print(response.text)
    return ss()
def ss():
    text = input("请输入说说：\n")
    get_time = round(int(time.time() * 1000))
    url = "https://weibo.com/aj/mblog/add?ajwvr=6&__rnd="+ str(get_time)
    print(url)
    print(session.cookies)

    data ={

        "location": "v6_content_home",
        "text": text,
        "appkey": "",
        "style_type": "1",
        "pic_id": "",
        "tid": "",
        "pdetail": "",
        "mid": "",
        "isReEdit": "false",
        "rank": "0",
        "rankid": "",
        "module": "stissue",
        "pub_source": "main_",
        "pub_type": "dialog",
        "isPri": "0",
        "_t": "0",
    }
    response = session.post(url=url,data=data,headers = HEADEAS).text
    print(response)
    return response


login()