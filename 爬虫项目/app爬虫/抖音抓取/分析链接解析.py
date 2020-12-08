import requests,time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree

from habdel_mongo import mongo_info1
url="https://v.douyin.com/JX1VsYG/"
user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
def get_html(url):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('user-agent={}'.format(user_agent))
    browser = webdriver.Chrome(chrome_options = chromeOptions)
    WebDriverWait(browser, 10)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    html=etree.HTML(html)
    douyin_info = {}
    douyin_info['dy_hao'] = html.xpath("//div//p[@class='unique_id--2sIkm']//text()")[0].split("：")[1].strip()
    text_list = html.xpath("//div//p[@class='right-text--GeDvB']//text()")
    douyin_info['dz']=int(float(text_list[0].replace("w",""))*10000)
    douyin_info['pp']=int(float(text_list[1].replace("w",""))*10000)
    douyin_info['paly_url'] = html.xpath("//div//video[@class='video-player--ORxFE hide--1XNRY']/@src")[0]
    print(douyin_info)
    mongo_info1.insert_item(douyin_info)
    page_url =browser.current_url
    urse_id = page_url.split("/?")[0].split("video/")[1]
    print(urse_id)
    return urse_id
urse_id=get_html(url)


url="https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids="+str(urse_id)
headers={
"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}

response=requests.get(url,headers=headers)
print(response.json())

