import requests,base64,json,re,time

headers = {
    "Host": "match.yuanrenxue.com",
    "Referer": "http://match.yuanrenxue.com/match/1",
    "User-Agent": "yuanrenxue.project",  # 比赛规定的请求头
    "X-Requested-With": "XMLHttpRequest",

}
def one():

    sum_=0
    for page in range(1,6):
        page_bas64=base64.b64encode('yuanrenxue{}'.format(page).encode()).decode('utf-8')
        # print(page_bas64)
        url="http://match.yuanrenxue.com/api/match/12?page={}&m={}".format(page,page_bas64)
        res=requests.get(url,headers=headers)
        # print(res.json())
        res=res.json()
        data=[ value['value'] for value in res['data']]
        print(sum(data))
        sum_ += sum(data)
    print(sum_)  #总和
# one()

def two():  #一个服务器返回cookie 和 生成cookie
    session =requests.session()
    session.headers=headers
    url ="http://match.yuanrenxue.com/match/13"
    res=session.get(url).text
    print(res)
    cookie= (re.findall(r'cookie=(.*?)\';path=',res)[0]).replace("('","").replace("')+","").replace("yuanrenxue_cookie=","")
    print(cookie)
    print(session.cookies)
    cookie={
        "yuanrenxue_cookie":cookie
    }
    sum_=0
    for page in range(1, 6):
        session.cookies.update=cookie
        url="http://match.yuanrenxue.com/api/match/13?page={}".format(page)

        res = session.get(url=url,cookies=cookie)
        print(res)
        res = res.json()
        data = [value['value'] for value in res['data']]
        print(sum(data))
        sum_ += sum(data)
    print(sum_)  # 总和
two()
import pywasm
def three():


    def env_abort(_: pywasm.Ctx):
        return

    vm = pywasm.load('./main.wasm', {
        'env': {
            'abort': env_abort,
        }
    })
    r = vm.exec('encode', [804134733,804134714])
    print(r)
three()