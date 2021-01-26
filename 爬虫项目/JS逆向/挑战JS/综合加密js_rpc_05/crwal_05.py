import requests
import json
import urllib3
urllib3.disable_warnings()  #去除证书警告
total = 0

for i in range(1,101):
    for j in range(1,7):
        print("第:"+ str(i)+"页\n")
        response = requests.get('http://sekiro.virjar.com/invoke?group=ws-chanllenge-15&action=getDate&num={}'.format(str(i)),verify=False).json()
        print(" response: " + json.dumps(response,ensure_ascii=False))
        if  response['status'] != 0:
            continue
        arrays = response['data']
        for item in arrays:
            num = item['value']
            total= total+ int(num)
        break

print("total: "+ str(total))