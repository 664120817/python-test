import requests,execjs,time,json


def get_m():
    with open("t.js",encoding='utf-8',mode='r') as f:
       js_code = f.read()
       m = execjs.compile(js_code).call("test")
       print(m)
       # print(m)
       return m
def handel_requests(page):
    url="http://match.yuanrenxue.com/api/match/2?page={}".format(page)
    headers={
"Host":"match.yuanrenxue.com",
"Cookie":get_m(),
"User-Agent":"yuanrenxue.project",  #比赛规定的请求头
"X-Requested-With":"XMLHttpRequest",
"Referer": "http://match.yuanrenxue.com/match/2"

}


    #不添加代理
    response = requests.get(url=url,headers=headers)
    print(response.text)
    # return response.json()
    # print(response.url)


if __name__ == '__main__':
  sum_num =0
  for page in range(1,6):
      res = handel_requests(page)
      data = [p['value'] for p in res['data']]
      sum_num +=sum(data)
      time.sleep(1)

  pass