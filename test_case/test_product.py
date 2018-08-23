# coding=utf-8
'''
商品详情V8
新增shippingInfo
新增sizeInfo
新增isSize
新增 wishQuantity
'''
import ConfigParser
import os
import json
import unittest
import requests
from mfilter import *

import time


class Run(unittest.TestCase):

    def setUp(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.abspath('.')+'/env.conf')

        self.conf = conf
        self.base_url = conf.get('env','momshop')
        self.user_token = conf.get('env','token')
        self.product_id = conf.get('product_id','id')
        self.product_id_error = conf.get('product_id','error_id')


    def test_001(self):
        '''商品详情--显示收藏数'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v8+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'AED'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1878'
        headers['Authorization'] = 'Beare' + self.user_token
        url = "/api/product?id=8316"
        response = requests.get(self.base_url+url,headers=headers)
        data = json.loads(response.text)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],"success")
        filter = Mfilter
        filter.run(data['data'], {
            'wishQuantity|int|require',
            'currency_units|varchar|require|inArray:["AED"]'
        })

    def test_002(self):
        '''商品详情--查看国家是否为阿联酋'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v8+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'AED'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1878'
        headers['Authorization'] = 'Beare' + self.user_token
        url = "/api/product?id=8316"
        response = requests.get(self.base_url+url,headers=headers)
        data = json.loads(response.text)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],"success")
        self.assertEqual(data['data']['shippingInfo']['country'], "United Arab Emirates")


    def test_003(self):
        '''商品详情--查看国家是否为沙特'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v8+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'AED'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1876'
        headers['Authorization'] = 'Beare' + self.user_token
        url = "/api/product?id=8316"
        response = requests.get(self.base_url+url,headers=headers)
        data = json.loads(response.text)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],"success")
        self.assertEqual(data['data']['shippingInfo']['country'], "Saudi Arabia")


    def test_004(self):
        '''商品详情--沙特国家的备货区间'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v8+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'AED'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1876'
        headers['Authorization'] = 'Beare' + self.user_token
        url = "/api/product?id=8316"
        response = requests.get(self.base_url+url,headers=headers)
        data = json.loads(response.text)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],"success")
        self.assertEqual(data['data']['shippingInfo']['country'], "Saudi Arabia")
        filter = Mfilter(self)
        filter.run(data['data']['shippingInfo'],{
            'date|varchar|require|inArray:["2018.08.18-2018.08.24"]'
        })

    def test_005(self):
        '''商品详情--查看阿联酋备货区间'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v8+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'AED'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1878'
        headers['Authorization'] = 'Beare' + self.user_token
        url = "/api/product?id=8316"
        response = requests.get(self.base_url+url,headers=headers)
        data = json.loads(response.text)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],"success")
        self.assertEqual(data['data']['shippingInfo']['country'], "United Arab Emirates")
        filter = Mfilter(self)
        filter.run(data['data']['shippingInfo'],{
            'date|varchar|require|inArray:["2018.08.16-2018.08.20"]'
        })

    def test_006(self):
        '''商品详情--查看沙特免邮金额'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v8+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'USD'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1876'
        headers['Authorization'] = 'Beare' + self.user_token
        url = "/api/product?id=8316"
        response = requests.get(self.base_url+url,headers=headers)
        data = json.loads(response.text)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],"success")
        self.assertEqual(data['data']['shippingInfo']['country'], "Saudi Arabia")
        filter = Mfilter(self)
        filter.run(data['data']['shippingInfo'],{
            'freeCost|int|require|inArray:[96]'
        })

    def test_007(self):
        '''商品详情--查看阿联酋免邮金额'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v8+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'USD'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1878'
        headers['Authorization'] = 'Beare' + self.user_token
        url = "/api/product?id=8316"
        response = requests.get(self.base_url+url,headers=headers)
        data = json.loads(response.text)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],"success")
        self.assertEqual(data['data']['shippingInfo']['country'], "United Arab Emirates")
        filter = Mfilter(self)
        filter.run(data['data']['shippingInfo'],{
            'freeCost|int|require|inArray:[64]'
        })


if __name__ =='__main__':
    unittest.main()