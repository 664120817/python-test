import requests,execjs,time,re

print(round(time.time()*1000))
sessions=requests.session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",

}
str_url= "http://eip.chanfine.com/resource/js/session.jsp?_={}&s_ajax=true".format(str(round(time.time()*1000)))


response=sessions.get(str_url,headers=headers)
# print(response.text)
str=re.findall(r'return "(.*?)";',response.text)[0]
print(str)
pwd="123456"
def get_pwd(str,pwd):
    with open("./js/cfw.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test",str,pwd)
       print("pwds:",pwds)
       return pwds


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
"Cookie": "JSESSIONID={}".format(str)
}
login_url="http://eip.chanfine.com/j_acegi_security_check"

data={"j_username":"664120817",
"j_password":get_pwd(str,pwd),
"j_redirectto":"",
}

response=requests.post(login_url,headers=headers,data=data)
print(response.url,response.text)