#-*- coding:utf-8 -*-

from selenium import webdriver
import time
import momshop_url.momshopURL

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os

class Chrome(object):

    #打开浏览器的方法
    def openWeb(self,url):

        #self.driver = webdriver.Chrome()
        self.Firefox = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(url)
        time.sleep(5)
        pass
    #关闭浏览器
    def closeChrome(self):
        self.driver.quit()
        pass

    #通过ID查找控件
    def FindID(self,ID):
        ids = (By.ID,ID)
        WebDriverWait(self.driver,20,0.5).until(EC.presence_of_all_elements_located(ids))
        return self.driver.find_element_by_id(ID)
        pass
    #通过Name查找控件
    def FindName(self,Name):
        names = (By.NAME,Name)
        WebDriverWait(self.driver,20,0.5).until(EC.presence_of_all_elements_located(names))
        return self.driver.find_element_by_name(Name)
        pass
    #通过className查找控件
    def Findclassname(self,ClassName):
        classnames = (By.CLASS_NAME,ClassName)
        WebDriverWait(self.driver,20,0.5).until(EC.presence_of_all_elements_located(classnames))
        return self.driver.find_element_by_class_name(ClassName)
        pass
    #通过xpath查找控件
    def FindXP(self,XP):
        xps = (By.XPATH,XP)
        WebDriverWait(self.driver,20,0.5).until(EC.presence_of_all_elements_located(xps))
        return self.driver.find_element_by_xpath(XP)
        pass

    #输入内容的方法
    def Input(self,type,value,inputvalue):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).send_keys(inputvalue)
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).send_keys(inputvalue)
        elif type == "id":
            self.driver.find_element_by_id(value).send_keys(inputvalue)
        elif type == "name":
            self.driver.find_element_by_name(value).send_keys(inputvalue)
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).send_keys(inputvalue)
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).send_keys(inputvalue)
        pass
    #鼠标事件方法一
    def Click(self,type,value):
        def Click(self, type, value):
            if type == "xpath":
                self.driver.find_element_by_xpath(value).click()
            elif type == "class_name":
                self.driver.find_element_by_class_name(value).click()
            elif type == "id":
                self.driver.find_element_by_id(value).click()
            elif type == "name":
                self.driver.find_element_by_name(value).click()
            elif type == "link_text":
                self.driver.find_element_by_link_text(value).click()
            elif type == "partial_link_text":
                self.driver.find_element_by_partial_link_text(value).click()
        pass
    def Clear(self,value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).clear()
        elif type == "id":
            self.driver.find_element_by_id(value).clear()
        elif type == "name":
            self.driver.find_element_by_name(value).clear()
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).clear()
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).clear()
        pass
    #验证元素是否存在
    def Check_element(self,type,value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value)
        elif type == "id":
            self.driver.find_element_by_id(value)
        elif type == "name":
            self.driver.find_element_by_name(value)
        elif type == "link_text":
            self.driver.find_element_by_link_text(value)
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value)
        pass

    # 获取子元素
    def Select_child_elements(self, type, value1, value2):
        if type == "xpath":
            Select(self.driver.find_element_by_xpath(value1)).select_by_visible_text(value2)
        elif type == "id":
            Select(self.driver.find_element_by_id(value1)).select_by_visible_text(value2)
        elif type == "name":
            Select(self.driver.find_element_by_name(value1)).select_by_visible_text(value2)
        elif type == "link_text":
            Select(self.driver.find_element_by_link_text(value1)).select_by_visible_text(value2)
        elif type == "partial_link_text":
            Select(self.driver.find_element_by_partial_link_text(value1)).select_by_visible_text(value2)
        pass

    # 获取输入框的值
    def Get_attribute(self, type, value1, value2):
        if type == "xpath":
            Value = self.driver.find_element_by_xpath(value1).get_attribute(value2)
            return Value
        elif type == "name":
            Value = self.driver.find_element_by_name(value1).get_attribute(value2)
            return Value
        elif type == "link_text":
            Value = self.driver.find_element_by_link_text(value1).get_attribute(value2)
            return Value
        elif type == "class_name":
            Value = self.driver.find_element_by_class_name(value1).get_attribute(value2)
            return Value
        elif type == "id":
            Value = self.driver.find_element_by_id(value1).get_attribute(value2)
            return Value
        pass

    # 显性等待时间
    def WebDriverWait(self, MaxTime, Mimtime, value):
        element = self.driver.find_element(By.ID, value)
        WebDriverWait(self.driver, MaxTime, Mimtime).until(EC.presence_of_element_located(element))
        pass

    # # 鼠标移动点击机制
    def Move_action(self, type, value):
        if type == "xpath":
            xm = self.driver.find_element_by_xpath(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "id":
            xm = self.driver.find_element_by_id(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "name":
            xm = self.driver.find_element_by_name(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "link_text":
            xm = self.driver.find_element_by_link_text(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        pass

    # 校验按钮是否为选中状态
    def Is_selected(self, type, value):
        if type == "id":
            self.driver.find_element_by_id(value).is_selected()
        elif type == "xpath":
            self.driver.find_element_by_xpath(value).is_selected()
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).is_selected()
        elif type == "name":
            self.driver.find_element_by_name(value).is_selected()
        elif type == "link_text":
         pass
    def FindDI(self):

        pass
        pass

