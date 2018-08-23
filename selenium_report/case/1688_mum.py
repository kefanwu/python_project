#!/usr/bin/env python
#encoding: utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
# from http.cookiejar import CookieJar
# import http.cookiejar
import time
import urllib
import sys
import os
import re
import csv
import random
import importlib
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

item_name = '水壶'
# 打开一个火狐浏览器
driver = webdriver.Firefox()

# 淘宝登录的url
login_url = 'https://login.taobao.com/member/login.jhtml'
# 淘宝用户名
tb_username = 'koukou890@qq.com'
# 淘宝密码
tb_password = 'rekoe@5382211'

# 跳转到登录页面
driver.get(login_url)
#放大火狐浏览器
driver.maximize_window()
# # 找到登录框右上角的标志，J_Quick2Static是切换到用户名密码登录的界面
# quick_2_static = driver.find_element_by_id('J_Quick2Static')
# # 如果J_Quick2Static显示了，说明现在是二维码登录界面，点击切换用户名密码登录界面
# if quick_2_static.is_displayed():
#     quick_2_static.click();
# 等待随机时间，以免被反爬虫
# time.sleep(random.uniform(0, 1))
# 找到账号登录框的DOM节点，并且在该节点内输入账号
# driver.find_element_by_name('TPL_username').send_keys(tb_username)
# # 等待随机时间，以免被反爬虫
# time.sleep(random.uniform(1, 2))
# # 找到账号密码框的DOM节点，并且在该节点内输入密码
# driver.find_element_by_name('TPL_password').send_keys(tb_password)
# # 等待随机时间，以免被反爬虫
# time.sleep(random.uniform(1, 2))

# # 找到登录窗口滑动验证的方块
# slider_square = driver.find_element_by_id('nc_1_n1z')

# # 判断方块是否显示，是则模拟鼠标滑动，否则跳过
# if slider_square.is_displayed():
#     # 鼠标点击滑块并保持
#     ActionChains(driver).click_and_hold(slider_square).perform()
#     # 鼠标多次向右移动随机距离
#     for i in range(0,5):
#         ActionChains(driver).move_by_offset(random.randint(60,80), 5).perform()
#     # 抬起鼠标左键
#     ActionChains(driver).release()
#     # 等待随机时间，以免被反爬虫
#     time.sleep(random.uniform(0, 1))

# # 找到账号登录框的提交按钮，并且点击提交
# driver.find_element_by_name('TPL_password').send_keys(Keys.ENTER)

# 睡眠5秒，防止未登录就进行了其他操作
time.sleep(15)
#取得cookie
driver.get_cookies()
#cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
#cookiestr = ';'.join(item for item in cookie)
#print(cookie)

url = 'https://xiertai.1688.com/page/offerlist_97586421.htm?spm=a2615.7691456.oldlist.2.8ca9fcf2byPfzf'

driver.get(url)
print driver.title
products = driver.find_element_by_xpath(".//*[@id='wp-all-offer-tab']/div/div[2]/div/div/div/ul[1]/li[1]/div[3]/a").text
print products
# 关闭模拟浏览器
driver.close()