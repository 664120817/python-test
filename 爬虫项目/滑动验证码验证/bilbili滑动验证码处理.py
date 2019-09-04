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
        self.user="664120817"
        self.pwd="******"
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

         # pages=self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="geetest-wrap"]/ul/li[5]/a[1]'))
        try:
         el_lock=self.driver.find_element_by_xpath('//*[@id="geetest-wrap"]/ul/li[5]/a[contains(@class,btn-login)]')
         # self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="geetest-wrap"]/ul/li[5]/a[1]')))
         el_lock.click()
        except Exception:
         pass
         # self.driver.execute_script("arguments[0].click();",el_lock)
         #定位图片对象
         img = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')
         time.sleep(3)
         #获取验证码图片对象坐标
         location =img.location
         print(location)
         #获取图片对象尺寸
         size=img.size
         print(size)
         # shot = self.get_screenshot()
         # print(shot.size)
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
        # 点击验证码拖动按钮
        # 等待错误提示信息消失
        # 屏幕截图
        # 抠验证码
        pass
    # 匹配本地对应原图
    def match_source(self,image):
        imagea = Image.open('1.png')
        imageb = Image.open('2.png')
        imagec = Image.open('3.png')
        imaged = Image.open('4.png')
        imagee = Image.open('5.png')
        imageg = Image.open('6.png')
        image7 = Image.open('7.png')
        list = [imagea,imageb,imagec,imaged,imagee,imageg,image7]
        # 通过像素差遍历匹配本地原图
        for li in list:
            # 原图与缺口图对应滑块图片横坐标相同，纵坐标原图比缺口图大px，可根据实际情况修改

            pixel1 = image.getpixel((252,154))
            pixel2 = li.getpixel((252,154))
            print(pixel1[0],pixel2[0],"像素")
            # pixel[0]代表R值，pixel[1]代表G值，pixel[2]代表B值
            if abs(pixel1[0] - pixel2[0]) < 5:
                print('第'+str(li)+'张图片' )
                return li
            else:
                print("匹配不成功")


    def is_pixel(self,image,image1,x,y):
        # pixel1=image.load()[x,y]
        # pixel2 = image1.load()[x, y]
        pixel1 = image.getpixel((x, y))
        pixel2 = image1.getpixel((x, y))
        print(pixel1,pixel2)
        #设置一个比较值
        threshold=80
        #比较
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self,image,image1):
        """
        核对两个验证码的相同位置的像素，找出像素偏差值大的位置，返回其C值，该值为验证码拖动的位移
        :param image: 没有阴影的验证码对象
        :param image1:有阴影的验证码图片
        :return:对比之后的偏移值
        """
        #
        left=80
        print(image.size)
        print(image.size[0],image.size[1])
        #遍历x抽的点到最后
        for i in range(left,image.size[0]):
            for j in range(image.size[1]):
                print(i,j)
                #获取一个坐标，在两张图上核对坐标的颜色差距，判断颜色差距是否过大，过大该X值为偏移值，返回值，否则继续
                if not self.is_pixel(image,image1,i,j):
                    print(i,"6666666666")
                    left = i
                    return round(left-8)  #round去除小数值
        return left

    # 滑块移动轨迹
    def get_track(self, offset):
        track = []
        current = 0
        mid = offset * 3 / 5
        t = random.randint(2, 3) / 10
        v = 0
        while current < offset:
            if current < round(mid):
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track
    def operate_button(self,track):
        #点击拖动按钮
        el_button=self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]/div[2]')
        ActionChains(self.driver).click_and_hold(el_button).perform()#点击按钮不放
        #移动滑块
        for i in track:
            ActionChains(self.driver).move_by_offset(xoffset=i,yoffset=0).perform()
        #松开按钮
        ActionChains(self.driver).release().perform()

    def do_captcha(self):
        #实现验证码处理
        #获取对应原图

        # 获取验证码图片 & 有阴影拼图的验证码图片
        img=self.get_image()
        # img = Image.open('captcha.png')
        img1 = self.match_source(img)
        # 比较两个验证码图片获取验证码块的偏移量

        offset=self.get_gap(img,img1)
        print(offset)
        # 使用偏移值计算移动操作
        track =self.get_track(offset)
        #操作滑块按钮，模拟拖动滑块做验证
        self.operate_button(track)
    def run(self):
        #主逻辑
        #来到登陆页面输入账号密码
        self.input_user_pwd()
        #处理验证码
        self.do_captcha()
if __name__== '__main__':
    bili=Bilibili()
    bili.run()