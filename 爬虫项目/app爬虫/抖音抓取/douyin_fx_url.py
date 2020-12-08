import json
from mitmproxy import ctx
num=0
def response(flow):
    print(flow.response.text)

    if "https://lf.snssdk.com/shorten/?" in flow.request.url:#分析链接
        num = +1
        print(flow.response.text)
        print(json.loads(flow.response.text))
        url=json.loads(flow.response.text).get('data')
        print(url,"88888888888888888888888")

        with open("url.txt","a") as f:
            f.write(url+",")