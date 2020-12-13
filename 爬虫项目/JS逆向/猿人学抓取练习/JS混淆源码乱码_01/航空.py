import requests,execjs,time,json


def get_m():
    with open("hk.js",encoding='utf-8',mode='r') as f:
       js_code = f.read()
       m = execjs.compile(js_code).call("test")
       print(m)
       m=m.replace('|','%E4%B8%A8')
       # print(m)
       return m
def handel_requests(page):
    url="http://match.yuanrenxue.com/api/match/1?page={}&m={}".format(page,get_m())
    headers={
# "Cookie":"__guid=201658765.569310395994656400.1607688675559.3142; monitor_count=5; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1607688941,1607690434,1607751584; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1607751584",
"Host":"match.yuanrenxue.com",
"Referer":"http://match.yuanrenxue.com/match/1",
"User-Agent":"yuanrenxue.project",  #比赛规定的请求头
"X-Requested-With":"XMLHttpRequest",

}


    #不添加代理
    response = requests.get(url=url,headers=headers)
    return response.json()
    # print(response.url)


if __name__ == '__main__':
    sum_num=0
    index_num =0
    for page in range(1,6):
        response=handel_requests(page)
        data=[p['value'] for p in response['data']]
        sum_num += sum(data)
        index_num += len(data)
        print( sum_num)
        time.sleep(1)

    average =sum_num/index_num
    print(average)
