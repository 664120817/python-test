import requests,time,json
session = requests.session()
headers= {

"Host":"match.yuanrenxue.com",
"Connection":"keep-alive",
"Content-Length":"0",
"User-Agent":"yuanrenxue.project",  #比赛规定的请求头
"Origin":"http://match.yuanrenxue.com",
"Accept":"*/*",
"Referer":"http://match.yuanrenxue.com/match/3",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",

}
def requests(page):
    session.headers=headers
    log_url ="http://match.yuanrenxue.com/logo"
    url= "http://match.yuanrenxue.com/api/match/3?page={}".format(page)
    respons= session.post(log_url)
    print(respons.cookies)
    respons= session.get(url)
    # print(respons.text)
    return respons.json()

if __name__ == '__main__':
    lists=[]
    for page in range(1,6):
      res=requests(page)
      value =[v['value'] for v in res['data']]
      lists +=value
      time.sleep(1)
    print(lists)
    print(max(lists, key=lists.count))