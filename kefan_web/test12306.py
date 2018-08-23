#-*- coding:UTF-8 -*-
#12306查询
import unittest,time
from selenium import webdriver
class TestGongxinban(unittest.TestCase):
    def setUp(self):
        print u"初始化"
        global dr
        dr = webdriver.Firefox()
        dr.maximize_window()
        dr.get("https://www.jd.com/")
        time.sleep(3)

    def tearDown(self):
        print u"结束清理"
        time.sleep(2)
        dr.quit()

    def testSearch(self):
        pass
    #     #搜索
    #     dr.find_element_by_xpath(".//*[@id='fmsearch']/input[3]").click()
    #     #获取弹框文本值
    #     print dr.switch_to_alert().text
    #     #关闭弹框
    #     dr.switch_to_alert().accept() #同意
    #     dr.switch_to_alert().dismiss() #取消
    #
    # def testSearch01(self):
    #     expValue = u"请填写注册名！"
    #     a = dr.current_window_handle
    #     print u"第一次获取句柄",a
    #     dr.find_element_by_xpath(".//*[@id='newLeft']/div[3]/a/img").click()
    #
    #     all1 = dr.window_handles
    #     print u"获取所有句柄",all1
    #     for t1 in all1:
    #         if t1 != a:
    #             print u"第二次获取句柄",t1
    #             dr.switch_to_window(t1)
    #     time.sleep(2)
    #     dr.find_element_by_xpath(".//*[@id='classfied1']/ul/li/table/tbody/tr[1]/th/a").click()
    #
    #     all2 = dr.window_handles
    #     print u"获取所有句柄:",all2
    #     for t2 in all2:
    #         if t2 != t1 and t2 != a:
    #             print u"第三次获取句柄",t2
    #             dr.switch_to_window(t2)
    #     time.sleep(2)
    #     dr.find_element_by_xpath(".//*[@id='agree']/span/ins").click()
    #
    #     dr.find_element_by_id("sendSm").click()
    #     time.sleep(2)
        #获取弹框文本值
        actValue =  dr.switch_to_alert().text
        try:
            self.assertEqual(actValue,expValue)
        except Exception:\
                assert False,\
                    "实际结果为:%s,预期结果为:%s" % (actValue,expValue)
        finally:
            #关闭弹框
            dr.switch_to_alert().accept() #同意

    def testSearch02(self):
        pass
        # dr.find_element_by_xpath(".//*[@id='indexLeftBL']/ul/li[1]/a/img").click()
        # dr.find_element_by_id("wf").click()
        # dr.find_element_by_id("fromStationText").send_keys(u"北京")
        # dr.find_element_by_id("toStationText").send_keys(u"上海")

        # 时间控件
        #输入出发日期
        #dr.find_element_by_id("train_date").send_keys("2016-6-28")
        #dr.find_element_by_id("back_train_date").send_keys(2016-6-29)
        #现在这个地方不可以直接输入了，可以通过js来输入
        #dr.execute_script("document.getElementById('train_date').setAttribute('value','2016-06-28')")
        #dr.execute_script("document.getElementById('back_train_date').setAttribute('value','2016-06-29')")
        #写有只读属性，则需要修改该属性，再通过js来输入
        # str1 = "document.getElementById(\"train_date\").readonly=false";
        # strDate1 = "document.getElementById(\"train_date\").value=\"2016-06-28\"";
        # dr.execute_script(str1)
        # dr.execute_script(strDate1)
        # str2 = "document.getElementById(\"back_train_date\").readonly=false";
        # strDate2 = "document.getElementById(\"back_train_date\").value=\"2016-06-29\"";
        # dr.execute_script(str2)
        # dr.execute_script(strDate2)
        #
        # dr.find_element_by_id("query_ticket").click()
        # time.sleep(2)


if __name__ == "__main__":
    unittest.main()
