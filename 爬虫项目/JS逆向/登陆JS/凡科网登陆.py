import requests,hashlib

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "143",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_cliid=3DLMt0zz7ZP8__S-; loginReferer=https://www.baidu.com/link?url=RSY27DTkSj6jGVX5UcLGSaeTkXE60-GB-3YAP99EZ2y&wd=&eqid=ff203880000922d4000000056062d6fa; loginComeForm=fkjz; first_ta=3; _ta=3; _tp=eqid%3Dff203880000922d4000000056062d6fa; _td=0 0 0 0; _newUnion=0; _kw=0; _audience=0; _haoci_rec_word=; _bidurl=; vid_url=; _vid_url=; _s_pro=i.fkw.com%2F; _c_pro=i.fkw.com%2F; ss_ta=3; wxRegBiz=none",
    "Host": "i.fkw.com",
    "Origin": "https://i.fkw.com",
    "Pragma": "no-cache",
    "Referer": "https://i.fkw.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",

}
url= "https://i.fkw.com/ajax/login_h.jsp?dogSrc=3"
pwd="123456"
def MD5_login(pwd):
    zt_pwd = hashlib.md5()
    zt_pwd.update(pwd.encode(encoding='utf-8'))
    print(zt_pwd.hexdigest())
    return zt_pwd.hexdigest()

data={
"cacct":"664120817",
"sacct":"",
"pwd":MD5_login(pwd),
"autoLogin":"false",
"staffLogin":"false",
"bizType":"5",
"dogId":"0",
"fromsite":"false",
"cmd":"loginCorpNews",

}

response=requests.post(url,data=data,headers=headers).text
print(response)