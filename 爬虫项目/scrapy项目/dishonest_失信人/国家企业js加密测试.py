import requests,re,js2py
index_url ='http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
#获取request 的session对象，可以自动合并cookie信息；
session=requests.session()
session.headers=headers #
#使用session 发送请求
response=session.get(index_url)
# print(response.status_code)
print(response.content.decode())
#1,提取script 标签中的js
js=re.findall(r'<script>(.*?)</script>',response.content.decode())[0]
print(js)
# 2，由于这种加密JS，最终指向的js代码，都是在eval函数中的，所以'{eval'(替换为){code=(， 然后就可以通过code,获取真正要执行的js了
js=js.replace('{eval(','{code=(')
#3,需要执行JS
# 3.1,获取执行js的环境
context=js2py.EvalJs()
context.execute(js)
#3.2 打印code的值
print(context.code)
#3.3获取生成Cookie的js
cookies_code=re.findall(r"document.(cookie=.*?)\+';Expires",context.code)[0]
# return _34.join('')})()+';Expires=Sun,
print(cookies_code)
#在js2py中，是不能使用 'document','window'这些浏览器中对象
#var _1a=document.createElement('div');_1a.innerHTML='<a href=\\'/\\'>_21</a>';_1a=_1a.firstChild.href
#js2py是无法处理的，需要能看懂上诉js代码
# var _34=document.createElement('div');_34.innerHTML='<a href=\'/\'>_15</a>';_34=_34.firstChild.href
# _34='http://www.gsxt.gov.cn'
# cookies_code=re.sub(r"var\s+(\w+)=document.createElement\('\w+'\);\w+.innerHTML='<a href=\\'/\\'>\w+</a>';\w+=\w+.firstChild.href",r"var /1='http://www.gsxt.gov.cn'",cookies_code)
cookies_code=re.sub(r"var\s+(\w+)=document.+?firstChild.href",r"var \1='http://www.gsxt.gov.cn'",cookies_code)
print(cookies_code)
#执行js，生成我们需要的cookie信息
context.execute(cookies_code)
#打印cookie
print(context.cookie)
# 上面用session.headers=headers添加headers，下面就不用传递headers
cookies=context.cookie.split('=')
# session.cookies.update({cookies[0]:cookies[1]})
session.cookies.set(cookies[0],cookies[1])#将JS的cokies 设置添加进去
session.get(index_url)#发送请求
print(session.cookies)
#获取cookie字典
cookies=requests.utils.dict_from_cookiejar(session.cookies)
print(cookies)


url='http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid=100000&noticeTitle=&regOrg='
data={
'draw': '3',
'start': '40',
'length': '10',
}

response=requests.post(url=url,cookies=cookies,data=data,headers=headers)
print(response.content.decode())
