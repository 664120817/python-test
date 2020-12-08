from selenium import webdriver
from selenium.webdriver.common.by import By
#WebDeriverWait 负责循环等待的
from selenium.webdriver.support.wait import WebDriverWait
#expected_conditions类  负责条件
from selenium.webdriver.support import  expected_conditions as EC
from selenium.common.exceptions import TimeoutException  #超时的异常
from urllib.parse import quote
from selenium.webdriver import ActionChains
import time
import re
# browser = webdriver.Chrome()
browser =webdriver.Chrome()
wait=WebDriverWait(browser,10)
KEYWORD='ipad'
url="https://s.taobao.com/search?q=ipad"
page=3
import pymysql
db=pymysql.Connect(host="localhost",port=3306,user="root",passwd="4786874",db="spider",charset="utf8")
cursor=db.cursor()

def indx_page(page):
     print("正在爬取第",page,"页")
     try:
        url = "https://s.taobao.com/search?q="+KEYWORD
        browser.get(url)
        if page>=1:
           input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager .form .input')))
           submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager .btn.J_Submit')))
           input.clear()
           input.send_keys(page)

           submit.click()

        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))#判断页码是否当前页码

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .item')))
        get_products()
     except TimeoutException:
         indx_page(page)
from pyquery import PyQuery as pq
def get_products():
    #提取网页数据
    html=browser.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product={
            'image':item.find('.pic .img').attr('data-src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
            'href':item.find('.row .J_ClickStat').attr('href'),
        }
        print(product['href'])
        image1=product['image']
        price1=product['price']
        deal=re.findall(r'.*(\d+).*', product['deal'])
        if deal :
           deal=deal[0]
        else:
            deal=str(0)
        sql = "delete from taobao"
        sql = "insert into taobao(image,price,title,deal,shop,location) values ('"+image1+"','"+price1+"','"+product['title']+"','"+deal+"','"+product['shop']+"','"+product['location']+"')"
        cursor.execute(sql)
        print(sql)

if  __name__ ==  '__main__':
    beginpage = int(input("请输入起始页"))
    endpage = int(input("请输入结束页"))
    for age in range(beginpage,endpage) :
         indx_page(age)
db.commit()
db.close()