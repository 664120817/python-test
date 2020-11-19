import requests,time,re,urllib
import execjs

import js2py
context=js2py.EvalJs()

session = requests.session()

user = ""
pwd =""

HEADEAS = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
def get_pwd(pwd):
    with open("./js/zzp.js") as f:
       js_code = f.read()
       pwds = execjs.compile(js_code).call("test", pwd)
       print(pwds)

    
       context.execute(js_code)
       p=context.test(pwd)

       print(p)


get_pwd(pwd)