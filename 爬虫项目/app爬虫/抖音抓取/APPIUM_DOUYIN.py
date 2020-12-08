from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time,multiprocessing
urse_id ='大碗宽面'
PLATFORM='Android'
DEVICE_NAME='127.0.0.1:62001'
APP_PACKAGK='com.ss.android.ugc.aweme'
APP_ACTIVITY='com.ss.android.ugc.aweme.splash.SplashActivity'
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
          'unicodeKeyboard': "True",  # 使用unicode输入法
          'resetKeyboard': "True",  # 重置输入法到初始状态
          'noReset': "True"  # 启动app时不要清除app里的原有的数据

        }



        # self.driver=webdriver.Remote(DRIVER_SERVER,self.desired_caps)
    def handle(self,device,port):
            print(device,port)
            desired_caps_duo = {
            "platformName":'Android',
            "platformVersion": '7.1.2',
            "deviceName":device,
            "appPackage": 'com.ss.android.ugc.aweme',
            "appActivity":'com.ss.android.ugc.aweme.splash.SplashActivity',
            "udid": device,
            # "automationName":AUTOMATION_NAME,
            'unicodeKeyboard': "True",  # 使用unicode输入法
            'resetKeyboard': "True",  # 重置输入法到初始状态
            'noReset': "True"  # 启动app时不要清除app里的原有的数据
        }

            self.driver = webdriver.Remote("http://localhost:"+str(port)+"/wd/hub",desired_caps_duo)

    def main(self,device,port):
        self.handle(device,port)
        x = self.driver.get_window_size()['width']  # 获取手机宽
        y = self.driver.get_window_size()['height']  # 获取手机高
        x1 = int(x * 0.5)
        y1 = int(y * 0.75)
        y2 = int(y * 0.25)
        time.sleep(10)
        self.driver.tap([(492,31),(524,63)],50)   #坐标点击 持续时间，单位毫秒，如：500
        try:
            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath('//android.widget.ImageView[@content-desc="搜索"]')): #定位搜索
                self.driver.find_element_by_xpath('//android.widget.ImageView[@content-desc="搜索"]').click()
        except:
            pass
        time.sleep(5)
        while True:
            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/ai5']")):
                self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/ai5']").click()
                self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/ai5']").send_keys(urse_id)
                while   self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/ai5']").text != str(urse_id):
                    self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/ai5']").click()
                    self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/ai5']").send_keys(urse_id)
                    time.sleep(0.3)
            self.driver.find_element_by_xpath("//android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView/android.view.View[1]/android.widget.TextView").click()
            time.sleep(3)
            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("//android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/androidx.appcompat.app.ActionBar.Tab[3]")):
               self.driver.find_element_by_xpath("//android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/androidx.appcompat.app.ActionBar.Tab[3]").click() #点击用户搜索
               time.sleep(1)
               self.driver.tap([(88,135),(166,156)],500)
            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("//android.widget.LinearLayout/android.view.View[1]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView")): #查看是否关注了，如果没就关注
                self.driver.find_element_by_xpath("//android.widget.LinearLayout/android.view.View[1]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView").click()

            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath("//android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.TextView[2]")):  # 点击粉丝
                self.driver.find_element_by_xpath("android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.TextView[2]").click()
                if "由于用户设置隐私,粉丝列表不可见" in self.driver.page_source:
                    self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/jk").click()
                    self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/ai5']").clear()
                    continue
            while True:
                self.driver.swipe(x1, y1, x1, y2)
                time.sleep(6)
                if "没有更多了" in self.driver.page_source:
                    break
                if "TA还没有粉丝" in self.driver.page_source:
                    break
            self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/jk").click()
            self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/jk").click()
            self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/ai5']").clear()



if __name__ == '__main__':
    moments = Moments()

    m_list=[]
    # devices_list =['127.0.0.1:62001','127.0.0.1:62025']
    devices_list = ['127.0.0.1:62026', '127.0.0.1:62027','127.0.0.1:62028']
    for device in range(len(devices_list)):
        port=4723+2*device #模拟器端口号会自动+2
        m_list.append(multiprocessing.Process(target=moments.main,args=(devices_list[device],port,)))
    for m1 in m_list:
        m1.start()
    for m2 in m_list:
        m2.join()

    #mitmdump 开启代理