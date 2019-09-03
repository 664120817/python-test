from io import BytesIO
from PIL import Image
from  selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
#expected_conditions类  负责条件
from selenium.webdriver.support import  expected_conditions as EC
from selenium.common.exceptions import TimeoutException  #超时的异常
from selenium.webdriver.common.by import By
#鼠标操作
from selenium.webdriver.common.action_chains import ActionChains
#等待时间 产生随机数
import time,random
class Bilibili(object):
    def __init__(self):
        self.driver=webdriver.Chrome()#创建浏览器对象
        self.driver.implicitly_wait(3)#隐士等待时间
        self.url ='https://passport.bilibili.com/login'
        self.user="13349851825"
        self.pwd="4786874"
        self.wait=WebDriverWait(self.driver,5)
    def input_user_pwd(self):
        #来登陆页面
        self.driver.get(self.url)
        el_user = self.driver.find_element_by_id('login-username')#定位
        el_user.send_keys(self.user)#设置内容
        el_pwd= self.driver.find_element_by_id('login-passwd')
        el_pwd.send_keys(self.pwd)
        self.get_position()
    def get_screenshot(self):
        #获取屏幕截图
        screentshot = self.driver.get_screenshot_as_png()#截图
        screentshot = Image.open(BytesIO(screentshot))#使用PIL将截图创建成 图片对象，该对象可以获取图片的相关信息
        return screentshot

    def get_position(self):
        #定位登陆钮，模拟点击
        try:
         el_lock=self.driver.find_element_by_xpath('//*[@id="geetest-wrap"]/ul/li[5]/a[contains(@class,btn-login)]')
         # self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="geetest-wrap"]/ul/li[5]/a[1]')))
         el_lock.click()
        except Exception:
         pass
         # self.driver.execute_script("arguments[0].click();",el_lock)
         #定位图片对象
         img = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')
         # img= self.driver.find_element_by_class_name('geetest_canvas_slice geetest_absolute')
         time.sleep(3)
         #获取验证码图片对象坐标
         location =img.location
         print(location)
         #获取图片对象尺寸
         size=img.size
         # print(size)
         #截取验证码的四条边
         left,top,right,button = location["x"],location["y"],location["x"]+size['width'],location["y"]+size['height']
         print(left,top,right,button)
         return  left,top,right,button

    def get_image(self):
        #获取两张验证码图片
        # 获取验证码的位置
        position=self.get_position()
        # 屏幕截图
        screenshot=self.get_screenshot()
        # 抠图没有滑块和阴影的验证码图片
        captcha =screenshot.crop(position)
        with open('captcha.png','wb')as f:
            captcha.save(f)
        return captcha

    def get_slider(self):
        """[summary]

        获取滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_track(self, distance):
        """[summary]

        根据偏移量获取移动轨迹

        Arguments:
            distance {[type]} -- 偏移量
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阀值
        mid = distance * 7 / 10
        # 计算间隔
        t = 0.15
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正
                a = 2.1
            else:
                # 加速度为负
                a = -4.8
            # 初速度v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0t + 1/2*a*t*t
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move, 2))
        return track

    def move_to_gap(self, slider, tracks):
        """[summary]

        拖动滑块到缺口处
        动作： 点击且不释放鼠标-拖拽图片到缺口-释放鼠标

        Arguments:
            slider {[type]} -- 滑块
            tracks {[type]} -- 轨迹
        """
        # 点击并按住滑块
        ActionChains(self.driver).click_and_hold(slider).perform()
        # 移动
        for x in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.1)
        # 释放滑块
        ActionChains(self.driver).release().perform()

    def is_try_again(self):
        """[summary]

        判断是否能够点击重试
        """
        button_text = self.driver.find_element_by_class_name('geetest_panel_error_title')
        text = button_text.text
        if text == '尝试过多':
            button = self.driver.find_element_by_class_name('geetest_panel_error_content')
            button.click()


    def is_success(self):
        """[summary]

        判断是否成功
        """
        button_text2 = self.driver.find_element_by_class_name('geetest_panel_success_title')
        text2 = button_text2.text
        if text2 == '通过验证':
            return 1
        return 0


    def for_move(self, x_temp):
        """[summary]

        循环拖动
        """
        flag = 0
        for i in range(0, 7):

            gap = random.randint(16, 20) * i + x_temp
            if gap < 40:
                continue
            print('预估计缺口位置: ', gap)
            self.is_try_again()
            slider = self.get_slider()
            track = self.get_track(gap)
            print('滑动轨迹: ', track)
            # 拖动滑块
            self.move_to_gap(slider, track)
            time.sleep(3)
            if self.is_success():
                flag = 1
                break
        return flag

    def crack(self):
        """[summary]

        验证
        """
        try:
            # 输入用户和密码
            self.input_user_pwd()
            # 获取验证码图片
            image1 = self.get_image()
            flag = 0
            while 1:
                temp = random.randint(0, 2)  # 将轨迹划分为2, 则有1/2的几率
                if temp == 0:
                    print('预估左1/2: ')
                    flag = self.for_move(0)
                else:
                    print('预估右1/2: ')
                    flag = self.for_move(120)
                if flag == 1:
                    break

        except TimeoutException as e:
            self.crack()



if __name__ == '__main__':
    bili = Bilibili()
    bili.crack()