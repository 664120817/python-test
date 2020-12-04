from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

PLATFORM='Android'
DEVICE_NAME='127.0.0.1:62001'
APP_PACKAGK='com.tal.kaoyan'
APP_ACTIVITY='com.tal.kaoyan.ui.activity.SplashActivity'
AUTOMATION_NAME ="UiAutomator1"
DRIVER_SERVER='http://localhost:4723/wd/hub'
TIMEOUT=3
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
          # "automationName":AUTOMATION_NAME,
          # 'unicodeKeyboard': "True",  # 使用unicode输入法
          # 'resetKeyboard': "True",  # 重置输入法到初始状态
          'noReset': "True"  # 启动app时不要清除app里的原有的数据

        }


        self.driver=webdriver.Remote(DRIVER_SERVER,self.desired_caps)
        try:
            if WebDriverWait(self.driver,TIMEOUT).until(lambda x:x.find_element_by_xpath("")): #是否跳过，有就点击，没有就跳过
                pass
        except Exception:
            pass
    def login(self):
        try:
            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("")):  # 是否跳过，有就点击，没有就跳过
                pass
        except Exception:
            pass
        try:
            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/login_code_touname']")):
                self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/login_code_touname']").click()
        except:
            pass

        try:
            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_email_edittext']")):
                self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_email_edittext']").send_keys("13349851825")
                self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_password_edittext']").send_keys("13349851825")
                self.driver.find_element_by_xpath("//android.view.View[@resource-id='com.tal.kaoyan:id/login_uname_login_btncover']").click()
        except:
            pass
        try:
              if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("//android.widget.CheckBox[@resource-id='com.tal.kaoyan:id/login_treaty_checkbox']")): #隐私协议勾选
                  self.driver.find_element_by_xpath("//android.widget.CheckBox[@resource-id='com.tal.kaoyan:id/login_treaty_checkbox']").click()
        except Exception:
            pass

        if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("//android.widget.RadioButton[@resource-id='com.tal.kaoyan:id/mainactivity_button_calendar']")):
            self.driver.find_element_by_xpath("//android.widget.RadioButton[@resource-id='com.tal.kaoyan:id/mainactivity_button_calendar']").click()
            self.driver.find_element_by_xpath("//android.widget.TextView[@text='研讯']").click()
    def slide(self):  #滑动
        x =self.driver.get_window_size()['width'] #获取手机宽
        y = self.driver.get_window_size()['height'] #获取手机高
        x1 =int(x*0.5)
        y1 =int(y*0.75)
        y2 = int(y*0.25)
        while True:
            self.driver.swipe(x1,y1,x1,y2)
            time.sleep(6)

    def main(self):
        """
        入口
        :return:
        """
        # 登录 首次登录需要用到login函数,第二次登录,请注释login
        self.login()
        time.sleep(3)
        self.slide()

if __name__ == '__main__':
    moments = Moments()
    moments.main()