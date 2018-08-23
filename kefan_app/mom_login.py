# coding=utf-8
from appium import webdriver
import time,unittest
class LoginTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appActivity'] = 'com.onemena.simsim.app.SplashActivity'
        desired_caps['appPackage'] = 'com.onemena.momshop'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        desired_caps['noReset'] = True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        '''免费礼物登录'''
        time.sleep(5)
        #点击首页免费礼物图片
        [617, 1184][677, 1244]
        self.driver.tap([([0,556]), (720,800)], 500)
        time.sleep(3)
        #点击getit跳转登录页面
        el1 = self.driver.find_element_by_id("com.onemena.momshop:id/iv_get_it")
        el1.click()
        #点击login按钮
        el2 = self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.onemena.momshop:id/tab_item_textview' and @text='Log In']")
        el2.click()
        time.sleep(3)
        #输入账号
        el3 = self.driver.find_element_by_id("com.onemena.momshop:id/et_email")
        el3.send_keys("wukefan@mom.com")
        #输入密码
        el4 = self.driver.find_element_by_id( "com.onemena.momshop:id/et_password")
        el4.send_keys("123456")
        time.sleep(3)
        #点击登录
        el5 = self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.onemena.momshop:id/tv_sign_up' and @text='Log In']")
        el5.click()
        time.sleep(3)
        self.assertEqual("Free Gifts",self.driver.find_element_by_xpath("//android.widget.TextView[@text='Free Gifts']").text)












if __name__ == "__main__":
    unittest.main()

