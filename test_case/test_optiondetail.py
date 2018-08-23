# coding=utf-8
'''
规格页v7接口
增加isSize
'''

import ConfigParser
import json
import os
import sys
import unittest
import requests
from mfilter import *
import random
import time
# import urllib2
# reload(sys)
# sys.setdefaultencoding("utf-8")


class Run(unittest.TestCase):

    def setUp(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.abspath('.') + '/env.conf')
        self.conf = conf
        self.base_url = conf.get('env', 'momshop')
        self.user_token = conf.get('env','token')


    def test_001(self):
        '''商品不展示尺码表'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v7+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'USD'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1878'
        headers['Authorization'] = 'Beare'+self.user_token
        url = "/api/product/productOptionDetail?product_id=4999"
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.text)
        value = json.dumps(data,ensure_ascii=False,indent=4)#json.dumps()用于将dict类型的数据转成str
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'],"success")
        self.assertEqual(data['data']['isSize'],False)
        filter = Mfilter(self)
        filter.run(data['data'], {
            'isSize|bool|require|inArray:[false]',
            'product_id|int|require|inArray:[4999]'
        })

    def test_002(self):
        '''商品展示尺码表'''
        headers = {}
        headers['Api-Version'] = 'application/vnd.momshop.v7+json'
        headers['lang'] = '1'
        headers['currencycode'] = 'AED'
        headers['channel-id'] = '4'
        headers['device-code'] = '642333e153271743'
        headers['country'] = '1878'
        headers['Authorization'] = 'Beare'+self.user_token
        url = "/api/product/productOptionDetail?product_id=5999"
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.text)
        value = json.dumps(data,ensure_ascii=False,indent=4)#json.dumps()用于将dict类型的数据转成str
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'],"success")
        self.assertEqual(data['data']['isSize'],True)
        filter = Mfilter(self)
        filter.run(data['data'], {
            'isSize|bool|require|inArray:[true]',
            'sizeImage|varchar|require',
            'product_id|int|require|inArray:[5999]'
        })

    def test001(self):
        shippingInfo= [{"country": "Saudi Arabia","date": "2018.08.18-2018.08.24","freeCost": "96"}]
        for item in shippingInfo:
            A = item['country']
            print A

shippingInfo = {"country": "Saudi Arabia", "date": "2018.08.18-2018.08.24", "freeCost": "96"}

print shippingInfo.items()[0]
for item in shippingInfo:
    print item +":"+str(shippingInfo[item])

if __name__=='__main__':
    unittest.main()