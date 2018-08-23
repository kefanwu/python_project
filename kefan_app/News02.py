#-*- coding:UTF-8 -*-
import time
from appium import webdriver
import unittest
from Share import Share
import HTMLTestRunner
class News02(unittest.TestCase):
    #封装初始化
    def setup(self):
        self.driver = Share().driver

    def tearDown(self):
        Share().tearDown()
    #评论用例
    def test001(self):
        Share().testcase003()


if __name__ == "__main__":
    unittest.main()
    # testunit = unittest.TestSuite()
    # testunit.addTest(unittest.makeSuite('testcase01'))  # 将测试用例加入到测试容器中
    # timestr = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))  # 本地日期时间作为测试报告的名字
    # filename = '/F:/test/Test-ZQ/report/' +timestr+ '.html'  # 这个路径改成自己的目录路径
    # fp = file(filename, 'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Report_title',
    #                                        description='Report_description')  # 使用HTMLTestRunner配置参数，输出报告路径、报告标题、描述
    # runner.run(testunit)  # 自动进行测试
    # fp.close()
