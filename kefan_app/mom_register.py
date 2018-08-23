# coding=utf-8
from appium import webdriver
import time, unittest

class RegisterTest(unittest.TestCase):
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

    def test_register(self):
        print "ok"
        '''个人中心--注册'''
        #点击tap个人中心
        self.driver.tap([(617,1184), (677,1244)], 500)
        #点击注册入口
        el1 = self.driver.find_element_by_id("com.onemena.momshop:id/tv_login")
        el1.click()
        #输入账号
        el2 = self.driver.find_element_by_id("com.onemena.momshop:id/et_email")
        el2.send_keys("111@111.com")
        #输入密码
        el3 = self.driver.find_element_by_id("com.onemena.momshop:id/et_password")
        el3.send_keys("123456")
        #点击注册按钮
        el3 = self.driver.find_element_by_name("Register")
        el3.click()
        #校验注册之后是否弹出优惠券提示框
        self.assertEqual("40.00 SAR",self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.onemena.momshop:id/tv_discount_amount' and @text='40.00 SAR']").text)






if __name__ == "__main__":
    unittest.main()