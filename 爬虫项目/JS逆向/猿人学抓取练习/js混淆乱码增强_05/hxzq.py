# -- coding: utf-8 --
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import time
import execjs
import os
import requests


def getTime():
    time.sleep(1)
    return str(int(time.time())) + '000'


m = str(int(time.time() * 1000 + 1000))
f = str(int(time.time())) + '000'
exec_bm = os.popen('node exec.js {}'.format(m)).read().replace('\n', '')
data = ''
for i in range(4):
    data += os.popen('node exec.js {}'.format(getTime())).read().replace('\n', ',')
data += os.popen('node m.js').read().replace('\n', '')
key = base64.b64encode(m[:-1].encode())
cryptor = AES.new(key=key, mode=AES.MODE_ECB)
data = base64.b64encode(cryptor.encrypt(pad(data.encode(), AES.block_size))).decode()
headers = {
    'cookie': 'm=' + exec_bm + ';RM4hZBv0dDon443M=' + data
}
url = 'http://match.yuanrenxue.com/api/match/5?page=3' + '&m=' + m + '&f=' + f
print(url)
response = requests.get(url, headers=headers)
print(response)