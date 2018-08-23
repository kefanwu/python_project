# _*_ coding:utf-8 _*_

import ConfigParser
import json
import os
import sys
import unittest
import requests
from mfilter import *
import random
import time
import urllib2
reload(sys)
sys.setdefaultencoding("utf-8")



class Run(unittest.TestCase):
    def setUp(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.abspath('.')+'/env.conf')
        self.conf=conf
        self.base_url = conf.get('evn','host')



# class Run(unittest.TestCase):
#     user_token = None
#     order_id = None
#
#     def __get_order_id(self):
#         if self.order_id==None:
#             self.order_id=self.order_store()
#         return self.order_id
#
#     def __get_user_token(self):
#         if self.user_token == None:
#             self.user_token = self.login()
#         return self.user_token
#
#     def setUp(self):
#         conf = ConfigParser.ConfigParser()
#         conf.read(os.path.abspath('.') + '/env.conf')
#         self.conf = conf
#         self.base_url = conf.get("env", "host")
#         self.channel_id = conf.get("app", "channel_id")
#         self.email =conf.get("app","email")
#         self.user_random_str = time.strftime("%Y%m%d", time.localtime())
#         self.lang=conf.get("app","lang")
#
#
#     def productOptions(self):
#         u'''商品详情加多规格'''
#         headers={}
#         headers['lang']=str(random.choice([1,3]))
#         headers['currencycode'] ='USD'
#         url = '/api/product?id=340'
#         response=requests.get(self.base_url+url,headers=headers,timeout=4)
#         data = json.loads(response.content)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['code'], 0)
#         for item in data['data']:
#             filter = Mfilter(self)
#             filter.run(item, {
#                 'product_id|int|require',
#                 'special|float|require',
#                 'discount|int|require',
#                 'save_price|float|require',
#                 'image|varchar|require',
#                 'imageMax|varchar|require'
#         })
#
#
#     def immediatebuy(self):
#         u'''立即购买确认订单接口'''
#         headers={}
#         headers['lang']='1'
#         headers['currencycode'] = 'USD'
#         url = '/api/product?id=26'
#         response=requests.get(self.base_url+url,headers=headers,timeout=3)
#         data = json.loads(response.content)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['code'], 0)
#         for item in data['data']['productOptions']:
#             filter = Mfilter(self)
#             filter.run(item, {
#                 'productOptionId|int|require',
#                 'price|float|require',
#                 'quantity|int|require',
#                 'name|varchar|require',
#                 'image|varchar|require',
#                 'imageMax|varchar|require'
#         })



if __name__ == "__main__":
    unittest.main()
