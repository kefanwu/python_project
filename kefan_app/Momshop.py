#-*- coding:UTF-8 -*-
from kefan_web import Common
import os
from Share import Share
import time
from appium import webdriver
from selenium import webdriver
import unittest
from kefan_web.Get_setup import Get_setup
class Momshop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "start now"
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appActivity'] = 'com.onemena.simsim.app.SplashActivity'
        desired_caps['appPackage'] = 'com.onemena.momshop'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        desired_caps['noReset'] = True
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)



    def test_cart_pay(self):
        '''【Momshop】下单流程'''
        Share.test001()

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()








