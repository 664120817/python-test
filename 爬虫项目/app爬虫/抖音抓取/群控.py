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
TIMEOUT=5
# MONGO_URL='localhost'
# MONGO_DB='moments'
# MONG0_COLLECTION='moments'
class Moments():

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

    def follow(self):
        try:
            # if WebDriverWait(self.driver, TIMEOUT).until(
            #         lambda x: x.find_element_by_xpath('//android.widget.RelativeLayout[@content-desc="关注"]/android.widget.ImageView')):  # 关注
            #     self.driver.find_element_by_xpath('//android.widget.RelativeLayout[@content-desc="关注"]/android.widget.ImageView').click()
            # if WebDriverWait(self.driver, TIMEOUT).until(
            #         lambda x: x.find_element_by_id('com.ss.android.ugc.aweme:id/b3n')):  # 点赞
            #         self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/b3n').click()
                    # self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/b40').click()
            # if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_id('com.ss.android.ugc.aweme:id/alk')):  # 评论
            #     self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/alk').click()
            #     self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/ald').click()
            #     self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/ald').send_keys("我来评论了")
            if WebDriverWait(self.driver, TIMEOUT).until(lambda x: x.find_element_by_xpath('//android.widget.ImageView[@content-desc="分享，按钮"]')):  # 分享
                    self.driver.find_element_by_xpath('//android.widget.ImageView[@content-desc="分享，按钮"]').click()
                    self.driver.find_element_by_xpath("//androidx.recyclerview.widget.RecyclerView[@resource-id='com.ss.android.ugc.aweme:id/c2']/android.widget.LinearLayout[7]").click()    #接合mitmdump 抓取分享链接
        except:
            pass
    def slide(self,device, port):  #滑动
        self.handle(device, port)
        x =self.driver.get_window_size()['width'] #获取手机宽
        y = self.driver.get_window_size()['height'] #获取手机高
        x1 =int(x*0.5)
        y1 =int(y*0.80)
        y2 = int(y*0.15)
        while True:
            print("滑动一次")
            time.sleep(10)
            try:
                self.driver.swipe(x1,y1,x1,y2)
                self.follow()
            except:
                continue

if __name__ == '__main__':
    moments = Moments()

    m_list=[]
    devices_list =['127.0.0.1:62001']
    # devices_list = ['127.0.0.1:62028', '127.0.0.1:62027']
    # devices_list = ['127.0.0.1:62026', '127.0.0.1:62027','127.0.0.1:62028','127.0.0.1:62029']
    for device in range(len(devices_list)):
        port=4723+2*device #模拟器端口号会自动+2
        m_list.append(multiprocessing.Process(target=moments.slide,args=(devices_list[device],port)))
    for m1 in m_list:
        m1.start()
    for m2 in m_list:
        m2.join()

    #mitmdump 开启代理