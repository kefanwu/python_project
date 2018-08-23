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
    user_token = None

    def __get_user_token(self):
        if self.user_token == None:
            self.user_token = self.login()
        return self.user_token

    def setUp(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.abspath('.')+'/env.conf')
        self.conf=conf
        self.base_url = conf.get('env','momshop')

    def login(self):
        u'''登录认证'''
        postData = {}
        postData['email'] = 'tester@2.com'
        postData['password'] = '123456'
        response = requests.post(self.base_url + '/api/login', data=postData)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)#字符串转成dict
        j = json.dumps(data,ensure_ascii=False,indent=4)#json.dumps()用于将dict类型的数据转成str
        print j
        self.assertEqual(data['code'], 0)
        self.user_token = data['data']['token']
        filter = Mfilter(self)
        filter.run(data['data'], {
            'token|varchar|require',
            'user|object|require'
        })

        return self.user_token



    def productOptions(self):
        u'''商品详情_V6'''
        headers={}
        headers['lang']="1"
        headers['currencycode'] ='USD'
        headers['Api-Version'] ='application/vnd.momshop.v6+json'
        headers['device-code'] = '111111'
        url = '/api/product?id=898'
        response=requests.get(self.base_url+url,headers=headers,timeout=4)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['data']['product_id'],898)
        filter = Mfilter(self)
        filter.run(data['data'], {
            'cartQuantity|int|require',
            'attributes|array|require',
            'activity_tip|varchar|require',
            'isGift|int|require',
            'serverGuarantee|array|require',
            'product_id|int|require',
            'discount|int|require',
            'is_wish|bool|require',
            'images_max|array|require',
            'images|array|require',
            'quantity|int|require',
            'name|varchar|require',
            'nameTag|array|require',
            'properties|array|require'
    })
        filter = Mfilter(self)
        for item in data['data']['properties']:
            filter.run(item, {
                'propertyId|int|require',
                'propertyName|varchar|require',
                'values|array|require'
        })
        for item in data['data']['properties']:
            values = item['values']
            for value in values:
                filter.run(value, {
                        'valueId|int|require',
                        'valueName|varchar|require',
                        'selected|bool|require'
                })

    def cart_add(self):
        u'''添加购物车_V2'''
        headers={}
        headers['lang']="1"
        headers['currencycode'] ='USD'
        headers['Api-Version'] ='application/vnd.momshop.v2+json'
        headers['device-code'] = '111111'
        url = '/api/cart/add?product_id=898&product_option_id=1006'
        response=requests.get(self.base_url+url,headers=headers,timeout=4)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'],'success')
        filter = Mfilter(self)
        filter.run(data['data'], {
            'totalPrice|floot|require',
            'quantity|int|require',
            'currency_units|varchar|require'
    })


    def getCartTotal(self):
        u'''购物车总计'''
        headers={}
        headers['lang']=str(random.choice([1,3]))
        headers['currencycode'] ='USD'
        headers['Authorization'] ='Bearer'+ self.__get_user_token()
        headers['device-code'] = '111111'
        url = '/api/cart/getCartTotal'
        response=requests.get(self.base_url+url,headers=headers,timeout=4)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'],'success')
        filter = Mfilter(self)
        filter.run(data['data'], {
            'totalPrice|floot|require',
            'quantity|int|require',
            'currency_units|varchar|require'
    })

    def getCart(self):
        u'''购物车列表'''
        headers = {}
        headers['lang'] = '1'
        headers['currencycode'] = 'USD'
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['device-code'] = '111111'
        headers['Api-Version'] = 'application/vnd.momshop.v6+json'
        url = '/api/cart/getCart'
        response = requests.get(self.base_url + url, headers=headers, timeout=4)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        filter = Mfilter(self)
        filter.run(data['data'], {
            'isFullReduction|int|require',
            'fullReductionNum|floot|require',
            'currencyUnits|varchar|require',
            'cartList|array|require',
            'anomalyCartList|array|require',
            'recommendSalesList|array|require',
            'cartTotal|object|require'
        })
        for item in data['data']['cartList']:
            cart_id = item['cart_id']
            filter.run(item, {
                'cart_id|int|require',
                'product_id|int|require',
                'product_option_id|int|require',
                'name|varchar|require',
                'product_option_name|varchar|require',
                'image|varchar|require',
                'quantity|int|require',
                'product_quantity|int|require',
                'stock|int|require',
                'status|int|require',
                'price|floot|require',
                'special|floot|require',
                'tax_class_id|int|require',
                'currency_units|varchar|require',
                'is_gift|int|require',
                'flag|int|require'
            })
            return cart_id

    def cart_upCart(self):
        u'''更新购物车数量_V6'''
        card_id=self.getCart()
        headers={}
        headers['lang'] = '1'
        headers['currencycode'] = 'USD'
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['device-code'] = '111111'
        headers['Api-Version'] = 'application/vnd.momshop.v6+json'
        products = [{"cart_id": card_id, "qty": 1,"product_id":898,"product_option_id":1006,"is_gift":0}]
        postdata = {}
        postdata['product_ids'] = json.dumps(products)
        url = '/api/cart/upCart'
        response = requests.post(self.base_url + url,headers=headers, data=postdata, timeout=4)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        filter = Mfilter(self)
        filter.run(data['data'], {
            'isFullReduction|int|require',
            'cartList|array|require',
            'anomalyCartList|array|require',
            'cartTotal|object|require',
            'recommendSalesList|array|require',
            'fullReductionNum|floot|require',
            'currencyUnits|varchar|require'
        })

    def api_checkout(self):
        '''确认订单_V6'''
        card_id = self.getCart()
        headers = {}
        headers['lang'] = '1'
        headers['currencycode'] = 'USD'
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['device-code'] = '111111'
        headers['Api-Version'] = 'application/vnd.momshop.v6+json'
        products = [{"cart_id": card_id, "qty": 1, "product_id": 898, "product_option_id": 1006, "is_gift": 0}]
        product_ids = json.dumps(products)
        url = "/api/checkout?product_ids="+str(product_ids)
        response =requests.get(self.base_url+url,headers=headers,timeout=4)
        data= json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertEqual(data['data']['codValid'], False)
        self.address_id= data['data']['addressInfo']['id']

        return self.address_id
        filter = Mfilter(self)
        filter.run(data['data'], {
            'discountPrice|int|require',
            'codValid|bool|require',
            'freightPrice|floot|require',
            'coupon|object|require',
            'vatPrice|floot|require',
            'cartList|array|require',
            'currencyUnits|varchar|require',
            'orderTotalPrice|floot|require',
            'addressInfo|object|require'

        })





    def order_store(self):
        '''提交订单_V3'''
        address_id = self.api_checkout()
        headers = {}
        headers['lang'] = '1'
        headers['currencycode'] = 'USD'
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['device-code'] = '111111'
        headers['Api-Version'] = 'application/vnd.momshop.v3+json'
        products = [{"qty": 1, "id": 898, "optId": 1006, "is_gift": 0, "flag": 0}]
        postdata={}
        product_ids = json.dumps(products)
        postdata['products'] = str(product_ids)
        postdata['address_id'] = str(address_id)
        postdata['channel_id'] = str(random.choice([3,4]))
        url = "/api/order/store"
        response =requests.post(self.base_url+url,headers=headers,data=postdata,timeout=5)
        data= json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')

        self.order_id = data['data']['order_id']
        return self.order_id
        filter = Mfilter(self)
        filter.run(data['data'], {
            'order_id|int|require'
        })



    # def order_pay(self):
    #     '''选择支付接口_V6'''
    #     order_id = self.order_store()
    #
    #     headers = {}
    #     headers['lang'] = '1'
    #     headers['currencycode'] = 'USD'
    #     headers['Authorization'] = 'Bearer' + self.__get_user_token()
    #     headers['device-code'] = '111111'
    #     headers['Api-Version'] = 'application/vnd.momshop.v6+json'
    #     url = "/api/order/pay?order_id=633"
    #     response = requests.get(self.base_url + url, headers=headers, timeout=5)
    #     data = json.loads(response.content)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['code'], 0)
    #     self.assertEqual(data['message'], 'success')
    #     self.assertEqual(data['data']['codValid'],False)
    #     filter = Mfilter(self)
    #     filter.run(data['data'], {
    #         'orderInfo|object|require',
    #         'payment|array|require'
    #     })
    #     print data.decode('raw_unicode_escape')
    #     for item in data['data']['orderInfo']:
    #         filter.run(item, {
    #             'products|array|require',
    #             'costDetail|array|require'
    #         })









