# coding=utf-8

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
    # user_token = None
    #
    # def __get_user_token(self):
    #     if self.user_token == None:
    #         self.user_token = self.login()
    #     return self.user_token

    def setUp(self):
        conf = ConfigParser.ConfigParser()
        print os.path.abspath('.')
        conf.read(os.path.abspath('.') + '/env.conf')
        self.conf = conf
        self.base_url = conf.get('env', 'momshop')

    def test_login(self):
        u'''登录认证'''
        headers = {}
        headers['device-code'] = '642333e153271743'
        postData = {}
        postData['email'] = 'tester@2.com'
        postData['password'] = '123456'
        response = requests.post(self.base_url + '/api/login',headers=headers,data=postData)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)#字符串转成dict
        print data
        # j = json.dumps(data,ensure_ascii=False,indent=4)#json.dumps()用于将dict类型的数据转成str
        # print j
        self.assertEqual(data['code'], 0)
        self.user_token = data['data']['token']
        filter = Mfilter(self)
        filter.run(data['data'], {
            'token|varchar|require',
            'user|object|require'
        })

        return self.user_token



    # def productOptions(self):
    #     u'''商品详情_V7'''
    #     headers={}
    #     headers['lang']="1"
    #     headers['currencycode'] ='USD'
    #     headers['Api-Version'] ='application/vnd.momshop.v7+json'
    #     headers['device-code'] = '642333e153271743'
    #     headers['Authorization'] = self.__get_user_token()
    #     url = '/api/product?id=4034'
    #     response=requests.get(self.base_url+url,headers=headers,timeout=4)
    #     data = json.loads(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['code'], 0)
    #     self.assertEqual(data['data']['product_id'],4034)
    #     self.assertEqual(data['data']['properties'][0]['showType'], "image")
    #     value = json.dumps(data['data']['productOptions'], ensure_ascii=False, indent=4)  # json.dumps()用于将dict类型的数据转成str
    #     filter = Mfilter(self)
    #     filter.run(data['data'], {
    #         'name|varchar|require',
    #         'image_cover|varchar|require',
    #         'images|array|require',
    #         'images_max|array|require',
    #         'price|float|require',
    #         'special|float|require',
    #         'is_wish|bool|require',
    #         'desciption|varchar|require',
    #         'attributes|array|require',
    #         'discount|int|require',
    #         'isOffSale|bool|require',
    #         'save_price|float|require',
    #         'rating|float|require',
    #         'serverGuarantee|array|require',
    #         'currency_units|varchar|require',
    #         'activity_tip|varchar|require',
    #         'cartQuantity|int|require',
    #         'isGift|int|require',
    #         'flag|int',
    #         'flashSale|array',
    #         'productOptions|array|require',
    #         'maxPrice|float|require',
    #         'freightPrice|float|require',
    #         'sales_quantity|int',
    #         'nameTag|array|require',
    #         'properties|array|require'
    # })
    #     for item in data['data']['properties']:
    #         filter.run(item, {
    #             'propertyName|varchar|require',
    #             'showType|varchar|require',
    #             'values|array|require',
    #             'propertyId|int|require'
    #             })
    #         for item in data['data']['properties'][0]['values']:
    #             filter.run(item, {
    #                 'image|varchar|require',
    #                 'valueId|int|require',
    #                 'selected|bool|require',
    #                 'valueName|varchar|require'
    #             })
    #     for item in data['data']['productOptions']:
    #         filter.run(item, {
    #             'productOptionId|int|require',
    #             'name|varchar|require',
    #             'price|float|require',
    #             'discount|int|require',
    #             'imageMax|varchar|require',
    #             'props|object|require',
    #             'image|varchar|require'
    #         })

    #
    # def productOptionDetail(self):
    #     u'''规格详情_V7'''
    #     print "wuekfan"
    #     headers = {}
    #     headers['lang'] = "1"
    #     headers['currencycode'] = 'USD'
    #     headers['Api-Version'] = 'application/vnd.momshop.v7+json'
    #     headers['device-code'] = '642333e153271743'
    #     headers['Authorization'] = self.__get_user_token()
    #     url = '/api/product/productOptionDetail?product_id=4034&product_option_id=25617'
    #     response = requests.get(self.base_url + url, headers=headers, timeout=4)
    #     data = json.loads(response.content)
    #     value= json.dumps(data,ensure_ascii=False, indent=4)
    #     self.assertEqual(data['code'],0)
    #     filter = Mfilter(self)
    #     filter.run(data['data'], {
    #         'product_id|int|require',
    #         'price|float|require',
    #         'special|float|require',
    #         'maxPrice|float|require',
    #         'currency_units|varchar|require',
    #         'productOptions|array|require',
    #         'properties|array|require'
    #     })
    #
    #     for item in data['data']['productOptions']:
    #         filter.run(item, {
    #             'productOptionId|int|require',
    #             'name|varchar|require',
    #             'price|float|require',
    #             'quantity|int|require',
    #             'image|varchar|require',
    #             'discount|int|require',
    #             'props|object|require'
    #             })
    #         self.assertEqual(data['data']['productOptions'][3]['productOptionId'],25617)
    #
    #     for item in data['data']['properties']:
    #         filter.run(item, {
    #             'propertyId|int|require',
    #             'propertyName|varchar|require',
    #             'linkName|varchar',
    #             'linkUrl|varchar',
    #             'values|array|require',
    #             'showType|varchar|require'
    #         })
    #         for item in data['data']['properties']:
    #             values = item['values']
    #             value = json.dumps(values, ensure_ascii=False, indent=4)
    #             # print value
    #             for value in values:
    #                 filter.run(value, {
    #                     'valueId|int|require',
    #                     'valueName|varchar|require',
    #                     'selected|bool|require',
    #                     'image|varchar'
    #               })

    # def promo_code(self):
    #     u'''验证优惠码'''
    #     headers = {}
    #     headers['lang'] = '1'
    #     headers['currencycode'] = 'USD'
    #     headers['Authorization'] = 'Bearer' + self.__get_user_token()
    #     headers['device-code'] = '642333e153271743'
    #     url = '/api/promo/code?code=2222&data=[{"id":4034,"optId":25617,"qty":20}]'
    #     response = requests.get(self.base_url + url, headers=headers, timeout=4)
    #     data = json.loads(response.text)
    #     value = json.dumps(data,ensure_ascii=False, indent=4)
    #
    #     self.assertEqual(data['code'],0)
    #     self.assertEqual(data['data']['coupon_type'],1)
    #     self.assertEqual(data['data']['title'],"Order 200+ $ ")
    #     self.assertEqual(data['data']['coupon_total'], 16)
    #     self.assertEqual(data['data']['is_available'], True)
    #
    # def coupon_get(self):
    #     u'''确认订单获取优惠码--满减类型接口'''
    #     headers = {}
    #     headers['lang'] = '1'
    #     headers['currencycode'] = 'USD'
    #     headers['Authorization'] = 'Bearer' + self.__get_user_token()
    #     headers['device-code'] = '642333e153271743'
    #     headers['Api-Version'] = 'application/vnd.momshop.v2+json'
    #     url = '/api/coupon/get?coupon_id=&data=[{"id":4034,"optId":25617,"qty":20}]'
    #     response = requests.get(self.base_url + url, headers=headers, timeout=4)
    #     data = json.loads(response.text)
    #     self.assertEqual(data['code'],0)
    #     values = data['data'][0]
    #     value = json.dumps(values, ensure_ascii=False, indent=4)
    #     for item in values:
    #         filter = Mfilter(self)
    #         filter.run(item, {
    #             'id|int|require',
    #             'coupon_total|int|require',
    #             'is_available|bool|require|inArray:[true]',
    #             'coupon_type|int|require|inArray:[1,2]',
    #             'discount_price|varchar|require',
    #             'discount|varchar|require|inArray:["","20% OFF"]'
    #         })
    #
    #
    # def my_coupons(self):
    #     u'''个人中心--折扣满减混合'''
    #     headers = {}
    #     headers['lang'] = '1'
    #     headers['currencycode'] = 'USD'
    #     headers['Authorization'] = 'Bearer' + self.__get_user_token()
    #     headers['device-code'] = '642333e153271743'
    #     headers['Api-Version'] = 'application/vnd.momshop.v2+json'
    #     url = '/api/coupon/my_coupons?type=unused'
    #     response = requests.get(self.base_url + url, headers=headers, timeout=4)
    #     data = json.loads(response.content)
    #     filter = Mfilter(self)
    #     self.assertEqual(data['code'],0)
    #     values = data['data']
    #     value = json.dumps(values, ensure_ascii=False, indent=4)
    #     for item in values:
    #         filter = Mfilter(self)
    #         filter.run(item, {
    #             'id|int|require',
    #             'unit|varchar|require|inArray:["$"]',
    #             'date|varchar|require',
    #             'coupon_total|int|require',
    #             'coupon_type|int|require|inArray:[1,2]',
    #             'discount_price|varchar|require',
    #             'title|varchar|require',
    #             'discount|varchar|require'
    #         })


if __name__=='__main__':
    unittest.main()

