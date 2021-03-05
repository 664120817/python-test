import requests,json,re,execjs
from lxml import etree
url="http://www.python-spider.com/challenge/11"

headers={

"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Cookie":"sessionid=miryvak2y92990yb4s3iktuk83ix6m4s; sign=1612790744178~1ccdb96a1a5638a5aef2fc97050f65be; Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1612693138,1612707458,1612788514,1612790745; no-alert=true; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1612797627; __jsl_clearance=1612797642.648|0|clD4VpfqhdaLBWywKWy%2FZyfi6d_60fae300e2cf760413ef486f1354aa3d3D",
"Host":"www.python-spider.com",
"Pragma":"no-cache",
"Referer":"http://www.python-spider.com/challenge/11",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",


}
session=requests.session()
response =session.get(url,headers=headers).text
js_text = re.findall(r"<script>(.*?)</script>",response)[0]
print(js_text)
sdk= """ function jsl_sdk(js_text){


setTimeout = function () {};
document = {};
document.cookie = "";
location={};
location.pathname = "/challenge/11";
location.search = "";
document.createElement = function (val) {
    return {
        innerHTML: "",
        firstChild: {
            href: "http://www.python-spider.com/",
        },
    }
};
window =global;
window.addEventListener = function () {};
document.addEventListener = function (a,b,c) {b()};
 document.attachEvent =function () {};
 eval(js_text)
 return document.cookie
 }
 """
res=execjs.compile(sdk).call("jsl_sdk",js_text)
print(res)
cookies = res.split(";")[0]
print(cookies)
# cookies=session.cookies
# cookies[res.split("=")[0]]= res.split("=")[1].split(";")[0]
headers={

"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Cookie":"sessionid=miryvak2y92990yb4s3iktuk83ix6m4s;{}".format(cookies),
"Host":"www.python-spider.com",
"Pragma":"no-cache",
"Referer":"http://www.python-spider.com/challenge/11",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",


}
response =requests.get(url,headers=headers).text
html=etree.HTML(response)
nums =html.xpath("//div//tr//td//text()")
num1=0
for num in nums:
 num1 +=int(num.strip())
print(num1)


# print(response)