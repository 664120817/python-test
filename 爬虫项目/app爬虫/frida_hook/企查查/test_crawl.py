import requests
import time
import json
import base64
import hook_sky

def req(url, params):
    header = {
      'Accept-Encoding': 'gzip',
      'User-Agent': 'com.tianyancha.skyeye/Dalvik/2.1.0 (Linux; U; Android 6.0; Nexus 6P Build/MDA89D; appDevice/google_QAQ_Nexus 6P)',
      'Content-Type': 'application/json',
      'channelID': 'YingYongBao',
      'deviceID': '{}'.format(params['deviceID']),
      'duid': '{}'.format(params['duid']),
      'tyc-hi': '{}'.format(params['tyc-hi']),
      'version': 'Android 11.4.0',
      'X-Auth-Token': '',
      'Authorization': '{}'.format(params['Authorization']),
      'Connection': 'close',
      'Host': 'api4.tianyancha.com'
    }
    r = requests.get(url, headers=header, verify=False, timeout=1.5)
    print(r.status_code)
    return r.text


def load():
    urls = set()
    with open('D:/code/test_decompile/skyeye/urls.txt', 'r') as f:
        for line in f:
            urls.add(line.strip())
    return urls

def to_file(ids, text):
    with open('D:/code/test_decompile/skyeye/'+ids, 'w') as f:
        f.write(text)

def start():
    base_url = 'https://api4.tianyancha.com/services/v3/t/details/appComIcV4/{}?pageSize=1000'
    script = hook_sky.hook_prepare()
    urls = load()
    for ids in urls:
       params = script.exports.getsig(base_url.format(ids), "Android 11.4.0")
       text = req(base_url.format(ids), params)
       to_file(ids, text)

start()

