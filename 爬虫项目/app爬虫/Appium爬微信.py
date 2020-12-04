import os
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time,re
from time import sleep
# from processor import Processor
# from config import *

# server='http://localhost:4723/wd/hub'
# desired_caps={
#   "platformName": "Android",
#   "deviceName": "MUCH_G2",
#   "appPackage": "com.tencent.mm",
#   "appActivity": ".ui.LauncherUI"
# }
#
# driver=webdriver.Remote(server,desired_caps)
# wait=WebDriverWait(driver,30)
# login=wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/cjk')))
# login.click()
# phone=wait.until(EC.presence_of_element_located((By.ID,"com.tencent.mm:id/h2")))
# phone.set_text('13349851825')
PLATFORM='Android'
DEVICE_NAME='MUCH_G2'
APP_PACKAGK='com.tencent.mm'
APP_ACTIVITY='.ui.LauncherUI'
DRIVER_SERVER='http://localhost:4723/wd/hub'
TIMEOUT=300
MONGO_URL='localhost'
MONGO_DB='moments'
MONG0_COLLECTION='moments'
class Moments():
    def __init__(self):
        #初始化，驱动配置
        self.desired_caps={
          "platformName": "Android",
          "deviceName": "127.0.0.1:62001",
          "appPackage": "com.tencent.mm",
          "appActivity": ".ui.LauncherUI",
         "automationName":"UiAutomator1",
        }

        self.driver=webdriver.Remote(DRIVER_SERVER,self.desired_caps)
        self.wait=WebDriverWait(self.driver,TIMEOUT)
        self.client=MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONG0_COLLECTION]
        # 处理器
        # self.processor = Processor()

    def login(self):
        """
        登录微信
        :return:
        """
        USERNAME='250588642'
        PASSWORD='8023hao??'
        # 登录按钮
        login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cjk')))
        login.click()
        # 手机输入
        phone = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/h2')))
        phone.set_text(USERNAME)
        # 下一步
        next = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/adj')))
        next.click()
        # 密码
        password = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/h2"][1]')))
        password.set_text(PASSWORD)
        # 提交
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/adj')))
        submit.click()

    def enter(self):
        """
        进入朋友圈
        :return:
        """
        # 选项卡
        tab = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/bw3"][3]')))
        tab.click()
        # 朋友圈
        moments = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/atz')))
        moments.click()



    def crawl(self):
        # 滑动点
        FLICK_START_X = 300,
        FLICK_START_Y = 300,
        FLICK_DISTANCE = 700,
        """
        爬取
        :return:
        """
        while True:
            # 当前页面显示的所有状态
            items = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@resource-id="com.tencent.mm:id/cve"]//android.widget.FrameLayout')))
            # 上滑
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            # 遍历每条状态
            for item in items:
                try:
                    # 昵称
                    nickname = item.find_element_by_id('com.tencent.mm:id/aig').get_attribute('text')
                    # 正文
                    content = item.find_element_by_id('com.tencent.mm:id/cwm').get_attribute('text')
                    # 日期
                    date = item.find_element_by_id('com.tencent.mm:id/crh').get_attribute('text')
                    # 处理日期
                    date = self.processor.date(date)
                    print(nickname, content, date)
                    data = {
                        'nickname': nickname,
                        'content': content,
                        'date': date,
                    }
                    print(data)
                    # 插入MongoDB
                    # self.collection.update({'nickname': nickname, 'content': content}, {'$set': data}, True)
                    # sleep(SCROLL_SLEEP_TIME)
                except NoSuchElementException:
                    pass

    def main(self):
        """
        入口
        :return:
        """
        # 登录 首次登录需要用到login函数,第二次登录,请注释login
        self.login()
        # 进入朋友圈
        self.enter()
        # 爬取
        self.crawl()



    def date(self, datetime):
        """
        处理时间
        :param datetime: 原始时间
        :return: 处理后时间
        """
        if re.match('\d+分钟前', datetime):
            minute = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', datetime):
            hour = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天', datetime):
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
        if re.match('\d+天前', datetime):
            day = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time()) - float(day) * 24 * 60 * 60)
        return datetime


if __name__ == '__main__':
    moments = Moments()
    moments.main()
