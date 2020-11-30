import requests,json,pymongo
import time
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor

from habdel_mongo import mongo_info
t=round(time.time())
print(time.time())

queue_list =Queue() #创建队列

#代理池
def get_porpy():
    try:
        response = requests.get('http://localhost:16888/random?protocol=http')
        if response.status_code == 200:
            ip = response.text
            print(ip)
            ips = {
                # "http":"http://117.191.11.110：8080",
                "http": ip
            }
            # response = requests.get(url="http://httpbin.org/ip", proxies=ips)
            response = requests.get(url="https://wh.zu.ke.com/zufang", proxies=ips)
            print(response.text)
            if response.status_code == 200:
                return ip
            else:
                get_porpy()
    except Exception:
        get_porpy()



def handel_requests(url,data):
    headers={

        # "Cookie": "duid=66712491",
        "client": "4",
        "version": "6972.2",
        "device": "LIO-AN00",
        "sdk": "22,5.1.1",
        "channel": "qqkp",
        "resolution": "960*540",
        "display-resolution": "960*540",
        "dpi": "1.0",
        # "pseudo-id": "ee34624e05871f86",
        "brand": "HUAWEI",
        "scale": "1.0",
        "timezone": "28800",
        "language": "zh",
        "cns": "2",
        "carrier": "CMCC",
        # "imsi": "460071642576844",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; LIO-AN00 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
        # "uuid": "dbf7a2f7-87a5-4c66-be6d-f9ce2c7c366b",
        "battery-level": "0.98",
        "battery-state": "3",
        "terms-accepted": "1",
        "newbie": "1",
        "reach": "1",
        "act-code": str(t),
        "act-timestamp": str(t+1),
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        "session-info": "PmFUwpJ6CXpufEQhP+/wFFUUCnLC4kwvc1XV0v2ThA4O7CYTnAkfhZ4Ykh+oOmueIeoN3HnJc8larLICdeRzfWkq5a4BXdAll+vggQZLarfXnHFiYDRi1j/96ZILO+Bi",
        "Host": "api.douguo.net",
        # "Content-Length": "132",
    }
    # #添加代理
    # proxies=get_porpy()
    # response = requests.post(url=url, headers=headers, data=data,proxies=)
    #不添加代理
    response = requests.post(url=url,headers=headers,data=data)
    return response

def handle_index():
    url = "https://api.douguo.net/recipe/flatcatalogs"

    data= {

        "client": "4",
        # "_session": "1606711834132866174168757686",
        # "v": "1606706090",
        "_vs": "2305",
        "sign_ran": "e21218137b1921546c8b20f1523ba8d5",
        # "code": "d08b57a9af7e0d99",
    }
    response =handel_requests(url=url,data=data)
    # print(response.text)
    response_josn= response.json()
    for items in response_josn.get('result').get('cs'):
        # print(items,"\n")
        name = items.get('name')
        print(name)
        for item in items.get('cs'):
            for i in item.get('cs'):
                 # print(i)
                 data1={
                    "client":"4",
                    # "_session":"1606719094615866174168757686",
                    "keyword":i.get('name'),
                    "order":"0",
                    "_vs":"400",
                    "type":"0",
                    "auto_play_mode":"2",
                    # "sign_ran":"fd6aad327b94822b7c940ad5a0b3908e",
                    # "code":"910ca9a426639330",

                 }
                 queue_list.put(data1)



def handle_caipu_list(data):
    print('当前处理的食材：',data.get('keyword'))
    # print(data)
    caipu_url="https://api.douguo.net/recipe/v2/search/0/20"
    caipu_response = handel_requests(url=caipu_url,data=data).json()
    # print(caipu_response)
    for item in caipu_response['result']['list']:
        caipu_info={}
        caipu_info['cailiao'] =data.get('keyword')
        if item['type']==13:
            caipu_info['user_name'] = item.get('r').get('an')
            caipu_info['pf'] = item.get('r').get('rate')
            caipu_info['zg'] = item.get('r').get('recommend_label')
            caipu_info['caipu_id'] = item.get('r').get('id')
            caipu_info['describe'] = item.get('r').get('cookstory')
            caipu_info['caipu_name'] = item.get('r').get('n')
            caipu_info['zuoliao_list'] = item.get('r').get('major')
            # print(caipu_info)
            """
            #做法详情,由于数据较大暂不插入
            detail_url ="https://api.douguo.net/recipe/v2/detail/"+str(caipu_info['caipu_id'])
            # print(detail_url)
            detail_data ={
                "client": "4",
                # "_session": "1606719094615866174168757686",
                "author_id": "0",
                "_vs": "11102",
                "_ext": '{"query":{"kw":'+str(caipu_info['cailiao'])+',"src":"11102","idx":"1","type":"13","id":'+str(caipu_info['caipu_id'])+'}}',
                "is_new_user": "1",
                # "sign_ran": "3420c395d26a04913763af7e13ef6876",
                # "code": "7b1ee363abda6f86",
            }
            # print(detail_data)
            detail_response = handel_requests(url=detail_url,data=detail_data).json()
            # print(detail_response)
            caipu_info['tips'] = detail_response['result']['recipe']['tips']
            caipu_info['cook_step'] =detail_response['result']['recipe']['cookstep']
           
            # print(json.dumps(caipu_info))
            """
            print(caipu_info)
            print("当前菜谱是：",caipu_info['caipu_name'])
            mongo_info.insert_item(caipu_info)

handle_index()
# print(queue_list.qsize())
pool =ThreadPoolExecutor(max_workers=20)
while queue_list.qsize()>0:
    pool.submit(handle_caipu_list,queue_list.get())

# handle_caipu_list(queue_list.get())