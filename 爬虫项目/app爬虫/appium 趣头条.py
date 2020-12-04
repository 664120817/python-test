from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time,re,random

# times = random.randint(45, 120)
PLATFORM='Android'
DEVICE_NAME='127.0.0.1:62001'
APP_PACKAGK='com.jifen.qukan'
APP_ACTIVITY='.login.V2MainLoginActivity'
AUTOMATION_NAME ="UiAutomator1"
DRIVER_SERVER='http://localhost:4723/wd/hub'
TIMEOUT=3000
# MONGO_URL='localhost'
# MONGO_DB='moments'
# MONG0_COLLECTION='moments'
class Moments():
    def __init__(self):
        #初始化，驱动配置
        self.desired_caps={
          "platformName": PLATFORM,
          "deviceName": DEVICE_NAME,
          "appPackage": APP_PACKAGK,
          "appActivity": APP_ACTIVITY,
          "automationName":AUTOMATION_NAME,
          # 'unicodeKeyboard': "True",  # 使用unicode输入法
          # 'resetKeyboard': "True",  # 重置输入法到初始状态
          # 'noReset': "True"  # 启动app时不要清除app里的原有的数据

        }


        self.driver=webdriver.Remote(DRIVER_SERVER,self.desired_caps)
        self.wait=WebDriverWait(self.driver,TIMEOUT)
        # self.client=MongoClient(MONGO_URL)
        # self.db = self.client[MONGO_DB]
        # self.collection = self.db[MONG0_COLLECTION]
    def login(self):
        """
        登录
        :return:
        """
        login = self.wait.until(EC.presence_of_element_located((By.ID,'com.jifen.qukan:id/brm')))
        login.click()
        print('0')
        sure =self.wait.until(EC.presence_of_element_located((By.ID,'com.jifen.qukan:id/a61')))
        sure.click()
        print('0.5')
        time.sleep(2)
        print("1")
        try:
            t = self.driver.find_element_by_id("com.jifen.qukan:id/ajo")
            t.click()
            el3 = self.driver.find_element_by_id("com.jifen.qukan:id/a1r");
            el3.click();
            print("2")
            time.sleep(30)
        except Exception:
            pass
        self.driver.press_keycode(4)
        # self.driver.back()
        # USERNAME='133498......'
        # PASSWORD=input("请输入验证码")
        # # 登录按钮
        # login = self.wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.EditText')))
        # time.sleep(10000)
        # login.click()
        # # 手机输入
        # phone = self.wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.EditText')))
        # phone.set_text(USERNAME)
        # time.sleep(10)
        # # 下一步
        # next = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.TextView')))
        # next.click()   #点击验证码
        # # 密码
        # pas = self.wait.until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.EditText')))
        # pas.click()
        # password = self.wait.until(
        #     EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.EditText')))
        # password.set_text(PASSWORD)
        # # 提交
        # submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.widget.Button')))
        # submit.click()


    def crawl(self):
        # 滑动点

        x = self.driver.get_window_size()['width']

        y = self.driver.get_window_size()['height']
        print(x,y)
        """
        爬取
        :return:
        """
        print("3")
        try:
            while True:

                # 当前页面显示的所有状态

                    # 上滑
                    self.driver.swipe(x*0.5, y*0.75, x*0.25,y*0.25,)
                    time.sleep(3)

                    # 选项卡
                    # t = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.view.View/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.ImageView")
                    t = self.driver.find_element_by_id("com.jifen.qukan:id/ajo")
                    t.click()
                    # print(times)
                    time.sleep(50)
                    self.driver.press_keycode(4)   # self.driver.back()

        except Exception:
            print("出错了")





    def main(self):
        """
        入口
        :return:
        """
        # 登录 首次登录需要用到login函数,第二次登录,请注释login
        self.login()
        # 爬取
        self.crawl()

if __name__ == '__main__':
    moments = Moments()
    moments.main()
