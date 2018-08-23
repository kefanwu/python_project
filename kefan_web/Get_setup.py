#-*- coding:UTF-8 -*-
from appium import webdriver
import unittest
from kefan_web.Common import singleton
@singleton
class Get_setup(unittest.TestCase):
    def __init__(self):
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