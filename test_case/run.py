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
# reload(sys)
# sys.setdefaultencoding("utf-8")


class Run(unittest.TestCase):
    user_token = None
    order_id = None

    def __get_order_id(self):
        if self.order_id==None:
            self.order_id=self.order_store()
        return self.order_id

    def __get_user_token(self):
        if self.user_token == None:
            self.user_token = self.login()
        return self.user_token

    def setUp(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.abspath('.') + '/env.conf')
        self.conf = conf
        self.base_url = conf.get("env", "host")
        self.channel_id = conf.get("app", "channel_id")
        self.email =conf.get("app","email")
        self.user_random_str = time.strftime("%Y%m%d", time.localtime())


    def register(self):
        u'''用户注册接口'''
        postData = {}
        postData['lang'] = random.randint(1, 3)  # id 1：en 2:zh-cn 3:ar
        postData['channel_id'] = random.randint(1, 4)  # 请求渠道id 1：pc站，2：H5手机站，3：ios-app，4：android-app
        postData['email'] = self.user_random_str +'wukefan@sim.com'
        postData['password'] = self.user_random_str
        postData['first_name'] = '1' + self.user_random_str
        postData['last_name'] = 'l' + self.user_random_str
        postData['device-code'] = '111111'
        response = requests.post(self.base_url + '/api/register', data=postData)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)
        self.assertNotEqual(data['data'], [])
        filter = Mfilter(self)
        filter.run(data['data'],{
            'token|varchar|require',
            'user|object|require'
        })



    def register_case01(self):
        u'''用户注册接口异常'''
        channel_id = self.channel_id.split(',')  # str转数组
        postData = {}
        postData['lang'] = random.randint(1, 3)  # id 1：en 2:zh-cn 3:ar
        postData['channel_id'] = channel_id[random.randint(0, 4)]
        postData['email'] = self.user_random_str + '@simsim.onemena1.com'
        postData['password'] = self.user_random_str
        postData['first_name'] = 'f' + self.user_random_str
        postData['last_name'] = 'l' + self.user_random_str
        postData['device-code'] = '111111'
        response = requests.post(self.base_url + '/api/register', data=postData)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)



    def login(self):
        u'''登录认证'''
        postData = {}
        postData['email'] = '15190257357@163.com'
        postData['password'] = '123456'
        response = requests.post(self.base_url + '/api/login', data=postData)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)
        self.user_token = data['data']['token']
        filter = Mfilter(self)
        filter.run(data['data'], {
            'token|varchar|require',
            'user|object|require'
        })
        return self.user_token


    def logout(self):
        u'''退出登录'''
        headers = {'Authorization': 'Bearer ' + self.__get_user_token()}
        response = requests.get(self.base_url + '/api/logout', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        filter = Mfilter(self)
        filter.run(data, {
            'data|object|require',
            'message|varchar|require'
        })




    def user(self):
        u'''用户信息'''
        headers={}
        headers['Authorization']='Bearer'+ self.__get_user_token()
        response = requests.get(self.base_url + '/api/user/',headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)
        filter = Mfilter(self)
        filter.run(data, {
            'data|object|require',
            'message|varchar|require'
        })


    def forget_password(self):
        u'''忘记密码'''
        postdata = {'email': '15190257357@163.com'}
        response = requests.post(self.base_url + '/api/forget_password', data=postdata)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'A new code has been sent to your email.')
        self.assertNotEqual(data['data']['email'], '')
        self.assertNotEqual(data['data']['customerId'], '')
        filter = Mfilter(self)
        filter.run(data, {
            'code|int|require',
            'data|object|require',
            'message|varchar|require'
        })
        filter.run(data['data'], {
            'customerId|int|require',
            'email|varchar|require'
        })


    def verification_code_post(self):
        u'''验证验证码是否有效'''
        code = "493501"
        postData = {}
        postData['code'] = code
        postData['customer_id'] = 11
        response = requests.post(self.base_url + '/api/check_verification_code', data=postData)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertEqual(data['data']['verificationCode'], '091002')
        self.assertEqual(data['data']['customerId'], '11')


    def setup_password(self):
        u'''重置密码'''
        postData = {}
        postData['customer_id'] = '11'
        postData['password'] = '000000'
        postData['confirm_password'] = '000000'
        response = requests.post(self.base_url + '/api/setup_password', data=postData)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertEqual(data['data'], {})
        filter = Mfilter(self)
        filter.run(data, {
            'code|int|require',
            'data|object|require',
            'message|varchar|require'
        })



    def category(self):
        u'''分类数据接口'''
        response = requests.get(self.base_url + "/api/category")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['code'], 0)
        self.assertNotEqual(data['data'], [])
        # print data
        for item in data['data']:
            self.valid_item(item)
    def valid_item(self, item):
        filter = Mfilter(self)
        filter.run(item, {
            'category_id|int|require',
            'image|varchar|require',
            'name|varchar|require',
            'children|array'
        })
        if 'children' in item and len(item['children']) > 0:
            for children in item['children']:
                self.valid_item(children)


    def product_category(self):
        u'''分类商品数据'''
        response = requests.get(self.base_url + "/api/product/category"+"?page=1&id=169")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['code'], 0)
        self.assertNotEqual(data['data'], [])
        for item in data['data']:
            filter = Mfilter(self)
            filter.run(item, {
                'product_id|int|require',
                'name|varchar|require',
                'price|float|require',
                'image_cover|varchar|require',
                'image_cover_middle|varchar|require	',
                'special|float|require',
                'discount|int|require',
                'is_stock|Bool|require',
                'wish_quantity|int|require',
                'is_wish|bool|require',
                'currency_units|varchar|require'
            })


    def product(self):
        u'''商品'''
        product_id = self.conf.get("app", "product_id")
        headers = {'Authorization': 'Bearer ' + self.__get_user_token()}
        response = requests.get(self.base_url + "/api/product", params={'id': product_id}, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(data['code'], 0)
        self.assertNotEqual(data['data'], [])


    def api(self):
        u'''首页数据接口'''
        url='/api?lang=2&channel_id=2&currency_code=*'
        response = requests.get(self.base_url + url)
        self.assertEqual(response.status_code,200)
        data=json.loads(response.text)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],'success')
        self.assertNotEqual(data['data'],{})
        filter = Mfilter(self)
        filter.run(data['data'],{
            'banner_info|object|require',
            'catagory_info|object|require'
        })


    def product(self):
        u'''商品详情'''
        headers={}
        headers['Authorization']='Bearer'+self.__get_user_token()
        headers['device-code']='1fac37e853c6eb74'
        url='/api/product?id=145'
        response = requests.get(self.base_url+ url,headers=headers)
        self.assertEqual(response.status_code, 200)
        data=json.loads(response.text)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], "success")
        self.assertNotEqual(data['data'],[])
        filter = Mfilter(self)
        filter.run(data['data'],{
            'product_id|int|require',
            'special|float|require',
            'discount|int|require',
            'save_price|float ',
            'is_wish|Bool|require',
            'name|varchar|require',
            'image_cover|varchar|require',
            'image_cover_max|varchar|require',
            'images|array|require',
            'images_max|array|require',
            'price|float |require',
            'is_stock|Bool|require',
            'descrption|varchar',
            'attributes|array',
            'discount|int'
        })



    def cart_add(self):
        u'''添加购物车'''
        headers={}
        headers['Authorization']='Bearer'+self.__get_user_token()
        url='/api/cart/add?product_id=145'
        response = requests.get(self.base_url+url, headers=headers)
        data= json.loads(response.text)
        # print data
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'], 'success')
        self.assertNotEqual(data['data'],[])
        filter = Mfilter(self)
        filter.run(data['data'], {
            'totalPrice|float|require',
            'quantity|int|require',
            'currency_units|varchar|require'

        })




    def cart_upcart(self):
        u'''更新购物车'''
        headers={}
        headers['Authorization']='Bearer'+self.__get_user_token()
        url= '/api/cart/upcart?quantity=11&product_id=145'
        response = requests.get(self.base_url+url,headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],'success')
        self.assertNotEqual(data['data'],[])
        filter= Mfilter(self)
        filter.run(data['data'],{
            'totalPrice|float|require',
            'quantity|int|require',
            'currency_units|varchar|require'

        })


    def cart_delcart(self):
        u'''删除购物车'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url = '/api/cart/delcart?product_id=145&add_wishlist=1'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertNotEqual(data['data'], [])
        self.assertEqual(data['data']['totalPrice'],0)
        self.assertEqual(data['data']['quantity'], 0)
        self.assertNotEqual(data['data']['currency_units'],[] )
        self.assertEqual(data['data']['successId'], "145")
        filter = Mfilter(self)
        filter.run(data['data'], {
            'totalPrice|int|require',
            'quantity|int|require',
            'currency_units|varchar|require',
            'successId|varchar|require',
            'failId|varchar|require'
        })




    def cart_null(self):
        u'''购物车为空时删除购物车'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url = '/api/cart/delcart?product_id=145&add_wishlist=1'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertNotEqual(data['data'], [])
        self.assertEqual(data['data']['totalPrice'],0)
        self.assertEqual(data['data']['quantity'], 0)
        self.assertNotEqual(data['data']['currency_units'],[] )
        self.assertEqual(data['data']['successId'], "")
        self.assertEqual(data['data']['failId'], "145")
        filter = Mfilter(self)
        filter.run(data['data'], {
            'totalPrice|int|require',
            'quantity|int|require',
            'currency_units|varchar|require',
            'successId|varchar|require',
            'failId|varchar|require'
        })



    def cart_getCart(self):
        u'''購物車詳細接口'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url = '/api/cart/getCart'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertNotEqual(data['data'], [])
        filter = Mfilter(self)
        filter.run(data['data'], {
            'cartList|array|require',
            'anomalyCartList|array|require',
            'recommendSalesList|array|require',
            'cartTotal|object|require'
        })



    def cart_getCartTotal(self):
        u'''獲取購物車總計信息'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url = '/api/cart/getCartTotal'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertNotEqual(data['data'], [])
        filter = Mfilter(self)
        filter.run(data['data'], {
            'totalPrice|float|require',
            'quantity|int|require',
            'currency_units|varchar|require'
        })


    def cart_upCartIos(self):
        u'''更新購物車IOS'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url = '/api/cart/upCartIos?product_id=145'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertNotEqual(data['data'], [])
        filter = Mfilter(self)
        filter.run(data['data'], {
            'cartInfo|object|require',
            'cartTotal|object|require'
        })
        filter.run(data['data']['cartTotal'], {
            'totalPrice|float|require',
            'quantity|int|require',
            'currency_units|varchar|require'
        })


    def wishlist_addOrDel(self):
        u'''添加删除收藏'''
        headers={}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['lang'] =str(random.randint(1, 3))
        headers['device-code'] = '1234567890'
        url='/api/wishlist/addOrDel?product_id=179&channel_id=3'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        filter = Mfilter(self)
        filter.run(data, {
            'data|object|require'
        })



    def api_wishlist(self):
        u'''我的收藏'''
        headers = {}
        headers['Authorization'] = 'Bearer'+self.__get_user_token()
        url = '/api/wishlist?page=1'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        self.assertNotEqual(data['data'], [])
        for item in data['data']:
            filter = Mfilter(self)
            filter.run(item, {
                'product_id|int|require',
                'name|varchar|require',
                'price|float|require',
                'image|varchar|require',
                'viewed|int|require',
                'quantity|int|require',
                'status|int|require',
                'is_wish|bool|require',
                'wishlist_total|int|require',
                'currency_units|varchar|require'
            })


    def select_address(self):
        u'''地址查询'''
        headers = {}
        headers['Authorization'] = 'Bearer'+self.__get_user_token()
        url='/api/select_address'
        response =requests.get(self.base_url+url,headers=headers)
        data=json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'], 'success')
        for item in data['data']['addressInfos']:
            # print item
            filter=Mfilter(self)
            filter.run(item,{
                'id|int|require',
                'customerId|int|require',
                'firstName|varchar|require',
                'lastName|varchar|require',
                'streetInfo|varchar|require',
                'countryId|int|require',
                'zoneId|int|require',
                'cityId|int|require',
                'districtId|int|require',
                'mobile|varchar|require',
                'addTime|varchar|require',
                'isDefault|int|require',
                'areaCode|varchar|require',
                'countryName|varchar|require',
                'countryDeep|int|require',
                'zoneName|varchar|require',
                'zoneDeep|int|require',
                'cityName|varchar|require',
                'cityDeep|int|require',
                'districtName|varchar|require',
                'districtDeep|int|require'
            })
            content = json.loads(response.content)['data']['addressInfos']
            for item in content:
                id = item['id']
                return id



    def update_address(self):
        u'''地址更新'''
        id=self.select_address()
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        postdata = {}
        postdata['address_id'] = str(id)
        postdata['first_name'] = 'scripscripscripscrip'
        postdata['last_name'] = 'scripscripscripscrip'
        postdata['country_id'] = '1878'
        postdata['zone_id'] = '2536'
        postdata['city_id'] = '233059'
        postdata['street_info'] = 'qwertyuiopqwertyuioqwertyuiopqwertyuiopqwertyuiop'
        postdata['mobile'] = '123123123'
        postdata['area_code'] = '971'
        url = '/api/update_address'
        response = requests.post(self.base_url + url, headers=headers, data=postdata)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        for item in data['data']['addressInfo']:
            filter = Mfilter(self)
            filter.run(item, {
                'id|int|require',
                'customerId|int|require',
                'firstName|varchar|require',
                'lastName|varchar|require',
                'streetInfo|varchar|require',
                'countryId|int|require',
                'countryName|varchar|require',
                'zoneId|int|require',
                'zoneName|varchar|require',
                'cityId|int|require',
                'cityName|varchar|require',
                'districtId|int|require',
                'districtName|varchar|require',
                'addTime|varchar|require',
                'mobile|varchar |require',
                'isDefault|int|require',
                'areaCode|varchar|require',
                'countryDeep|int|require',
                'zoneDeep|int|require',
                'cityDeep|int|require',
                'districtDeep|int|require'
            })


    def delete_address(self):
        u'''删除地址'''
        id = self.select_address()
        headers={}
        headers['Authorization']='Bearer '+ self.__get_user_token()
        url = self.base_url+'/api/delete_address?address_id='+str(id)
        response = requests.get(url,headers=headers)
        data=json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'],'success')
        self.assertNotEqual(data['data'],[])
        self.assertEqual(data['data']['deleteNum'],1)
        filter=Mfilter(self)
        filter.run(data['data'],{
            'deleteNum|int|require',
            })



    def insert_address(self):
        u'''新增地址'''
        headers = {}
        postdata={}
        postdata['first_name']='wukefan'
        postdata['last_name'] = 'om'
        postdata['country_id'] = '1878'
        postdata['zone_id'] = '2536'
        postdata['city_id'] = '233059'
        postdata['street_info'] = '<script>alert(document.cookie)</script>'
        postdata['mobile'] = '123213232'
        postdata['area_code'] = '971'
        postdata['is_default'] = '0'
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url = '/api/insert_address'
        response = requests.post(self.base_url + url, headers=headers,data=postdata)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], 'success')
        for item in data['data']['addressInfo']:
            filter = Mfilter(self)
            filter.run(item, {
                'id|int|require',
                'customerId|int|require',
                'firstName|varchar|require',
                'lastName|varchar|require',
                'streetInfo|varchar|require',
                'countryId|int|require',
                'countryName|varchar|require',
                'zoneId|int|require',
                'zoneName|varchar|require',
                'cityId|int|require',
                'cityName|varchar|require',
                'districtId|int|require',
                'districtName|varchar|require',
                'addTime|varchar|require',
                'mobile|varchar |require',
                'isDefault|int|require',
                'areaCode|varchar|require',
                'countryDeep|int|require',
                'zoneDeep|int|require',
                'cityDeep|int|require',
                'districtDeep|int|require'
            })


    def area_info(self):
        u'''国家城市信息联查'''
        headers={}
        headers['Authorization']= 'Bearer '+self.__get_user_token()
        url= '/api/area_info'
        response =requests.get(self.base_url+url,headers=headers)
        data= json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'], "success")
        self.assertNotEqual(data['data'], [])
        self.assertNotEqual(data['data']['areaInfo'], [])
        for item in data['data']['areaInfo']:
            filter=Mfilter(self)
            filter.run(item,{
                'id|int|require',
                'name|varchar|require',
                'parentId|int|require',
                'code|varchar|require',
                'deep|int|require',
                'subset|int|require',
                'areaCode|varchar|require'
            })



    def coupon_verify(self):
        u'''立即购买--验证优惠码接口'''
        headers={}
        headers['Authorization']='Bearer'+self.__get_user_token()
        url='/api/coupon/verify?code=1111&type=2&product_id=145&quantity=8'
        response=requests.get(self.base_url+url,headers=headers)
        data=json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['code'],0)
        self.assertEqual(data['message'], "success")
        self.assertNotEqual(data['data']['discount'],[])


    def Cart_coupon_verify(self):
        u'''購物車--验证优惠码接口'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url = '/api/coupon/verify?code=1111'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], "success")
        self.assertNotEqual(data['data']['discount'], [])




    def api_checkout(self):
        u'''购物车确认订单'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url='/api/checkout'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], "success")
        filter = Mfilter(self)
        filter.run(data['data'], {
            'discountPrice|int|require',
            'freightPrice|float|require',
            'currencyUnits|varchar|require',
            'orderTotalPrice|float|require'
        })
        filter.run(data['data']['cartTotal'], {
            'currencyUnits|varchar|require',
            'totalPrice|float|require',
            'quantity|int|require'
        })
        filter.run(data['data']['addressInfo'], {
            'id|int|require',
            'customerId|int|require',
            'firstName|varchar|require',
            'lastName|varchar|require',
            'streetInfo|varchar|require',
            'countryId|int|require',
            'zoneId|int|require',
            'cityId|int|require',
            'districtId|int|require',
            'mobile|varchar|require',
            'addTime|varchar|require',
            'isDefault|int|require',
            'areaCode|varchar|require',
            'countryName|varchar|require',
            'countryDeep|int|require',
            'zoneName|varchar|require',
            'zoneDeep|int|require',
            'cityName|varchar|require',
            'cityDeep|int|require'
        })
        for item in data['data']['cartList']:
            filter.run(item, {
                'status|int|require',
                'name|varchar|require',
                'image|varchar|require',
                'tax_class_id|int|require',
                'currency_units|varchar|require',
                'price|float|require',
                'product_id|int|require',
                'product_quantity|int|require',
                'stock|int|require',
                'cart_id|int|require',
                'special|float|require',
                'quantity|int|require'
            })


    def api_immediatebuy(self):
        u'''立即购买--确认订单'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        url = '/api/immediatebuy?product_id=145'
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], "success")
        self.assertNotEqual(data['data']['product'],[])
        for item in data['data']['product']:
            self.assertEqual(item['product_id'], 145)
            filter = Mfilter(self)
            filter.run(item,{
                'product_id|int|require',
                'name|varchar|require',
                'image|varchar|require',
                'quantity|int|require',
                'product_quantity|int|require',
                'stock|int|require',
                'status|int|require',
                'price|float|require',
                'special|float|require',
                'currency_units|varchar|require',
                'total|float|require'
            })

    def order_store(self):
        u'''提交订单'''
        qty=random.randint(1,60)
        products = [{"id":145,"qty":qty}]
        id=self.select_address()
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        postdata={}
        postdata['address_id']=str(id)
        postdata['channel_id'] = '3'
        postdata['products']= json.dumps(products)
        url = '/api/order/store'
        response = requests.post(self.base_url + url,data=postdata,headers=headers,)
        data = json.loads(response.content)
        self.order_id=data['data']['order_id']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertNotEqual(data['data']['order_id'],[] )
        self.assertNotEqual(data['data'], [])
        filter = Mfilter(self)
        filter.run(data['data'], {
            'order_id|int|require'
        })
        return self.order_id



    def immediateBuy(self):
        u'''立即购买--提交订单'''
        id=self.select_address()
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        postdata={}
        postdata['channel_id']=str((random.randint(2, 4)))
        postdata['address_id']=str(id)
        url = '/api/order/immediateBuy?product_id=145'
        response = requests.post(self.base_url + url, headers=headers,data=postdata)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertNotEqual(data['data']['order_id'], [])
        self.assertNotEqual(data['data'], [])
        filter = Mfilter(self)
        filter.run( data['data'], {
            'order_id|int|require'
        })


    def order_list(self):
        u'''(post)用户中心-订单列表查询多条'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['channel_id'] = str(random.randint(2, 4))
        headers['lang'] = str(random.randint(1, 3))
        headers['currencycode'] = 'usd'
        postdata={}
        postdata['page']='1'
        postdata['limit'] = '21'
        url = '/api/order/list'
        response = requests.post(self.base_url + url, headers=headers,data=postdata)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        filter = Mfilter(self)
        filter.run( data['data'], {
            'total|int|require',
            'orders|array|require'
        })
        for item in data['data']['orders']:
            filter = Mfilter(self)
            filter.run(item, {
                'orderId|int|require',
                'orderSn|varchar|require',
                'status|varchar|require',
                'orderStatusId|int|require',
                'addTime|varchar|require',
                'totalPrice|float|require',
                'currencyUnits|varchar|require',
                'productNum|int|require',
                'products|array|require'
            })


    def order_list_status_1(self):
        u'''(get)用户中心-订单列表查询单条状态1'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['channel_id'] = str(random.randint(2, 4))
        headers['lang'] = str(random.choice([1, 3]))
        headers['currencycode'] = 'usd'
        postdata = {}
        postdata['order_status_id']='1'
        postdata['page'] = '1'
        postdata['limit'] = '21'
        url = '/api/order/list'
        response = requests.post(self.base_url + url, headers=headers,data=postdata)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        filter = Mfilter(self)
        filter.run(data['data'], {
            'total|int|require',
            'orders|array|require'
        })
        if data['data']['total']==0:
            self.__get_order_id()
        else:
            for item in data['data']['orders']:
                self.assertEqual(item['orderStatusId'],1)
                filter = Mfilter(self)
                filter.run(item, {
                    'orderId|int|require',
                    'orderSn|varchar|require',
                    'status|varchar|require',
                    'orderStatusId|int|require',
                    'addTime|varchar|require',
                    'totalPrice|float|require',
                    'currencyUnits|varchar|require',
                    'productNum|int|require',
                    'products|array|require'
                })





    def order_detail01(self):
        u'''(get)用户中心-订单详情'''
        orderId=self.__get_order_id()
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['lang'] = '3'
        headers['currencycode'] = 'usd'
        url = '/api/order/detail?order_id='+str(orderId)
        response = requests.get(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        self.assertEqual(data['message'], "success")
        filter = Mfilter(self)
        filter.run(data['data'], {
            'orderInfo|object|require'
        })

        filter.run(data['data']['orderInfo'], {
            'products|array|require',
            'costDetail|array|require'
        })

        filter.run(data['data']['orderInfo'], {
            'id|int|require',
            'orderSn|varchar|require',
            'paymentMethod|varchar|require',
            'orderStatusId|int|require',
            'status|varchar|require',
            'dateAdded|varchar|require',
            'total|float|require',
            'currencyCode|varchar|require',
            'currencyValue|varchar|require',
            'shippingCountry|varchar|require',
            'shippingZone|varchar|require',
            'shippingCity|varchar|require',
            'shippingAddress1|varchar|require',
            'lastname|varchar|require',
            'firstname|varchar|require',
            'telephone|varchar|require',
            'theTimeCountdown|int|require',
            'theTimeStampCountdown|int|require',
            'currencyUnits|varchar|require'
        })


    def order_detail02(self):
        u'''(post)用户中心-订单详情'''
        orderId = self.__get_order_id()
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['lang'] = '3'
        headers['currencycode'] = 'usd'
        postdata={}
        postdata['order_id']=str(orderId)
        url = '/api/order/detail'
        response = requests.post(self.base_url + url, headers=headers,data=postdata)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        filter = Mfilter(self)
        filter.run(data['data'], {
            'orderInfo|object|require'
        })
        filter.run(data['data']['orderInfo'], {
            'products|array|require',
            'costDetail|array|require'
        })
        filter.run(data['data']['orderInfo'], {
            'id|int|require',
            'orderSn|varchar|require',
            'paymentMethod|varchar|require',
            'orderStatusId|int|require',
            'status|varchar|require',
            'dateAdded|varchar|require',
            'total|folat|require',
            'currencyCode|varchar|require',
            'currencyValue|varchar|require',
            'shippingCountry|varchar|require',
            'shippingZone|varchar|require',
            'shippingCity|varchar|require',
            'shippingAddress1|varchar|require',
            'lastname|varchar|require',
            'firstname|varchar|require',
            'telephone|varchar|require',
            'theTimeCountdown|int|require',
            'theTimeStampCountdown|int|require',
            'currencyUnits|varchar|require'
        })


    def order_cancel(self):
        u'''(post)订单取消'''
        orderId = self.__get_order_id()
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['lang'] = '3'
        headers['currencycode'] = 'usd'
        postdata = {}
        postdata['order_id'] = str(orderId)
        postdata['cancel_reason'] = u"没钱？为什么没钱"
        url = '/api/order/cancel'
        response = requests.post(self.base_url + url, headers=headers, data=postdata)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        filter = Mfilter(self)
        filter.run(data, {
            'data|object|require'
        })


    def order_list_status_5(self):
        u'''(get)查询状态5订单，返回'''
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['channel_id'] = str(random.randint(2, 4))
        headers['lang'] = '3'
        headers['currencycode'] = 'usd'
        url = '/api/order/list?order_status_id=5&page=1&limit=21'
        response = requests.post(self.base_url + url, headers=headers)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        content = json.loads(response.content)['data']['orders']
        for item in content:
            orderId = item['orderId']
        return orderId


    def order_repurchase(self):
        u'''订单-再次购买'''
        orderId= self.order_list_status_5()
        headers = {}
        headers['Authorization'] = 'Bearer' + self.__get_user_token()
        headers['lang'] = '3'
        headers['currencycode'] = 'usd'
        postdata = {}
        postdata['order_id'] = str(orderId)
        postdata['cancel_reason'] = u"我不想买了，没钱"
        url = '/api/order/repurchase'
        response = requests.post(self.base_url + url, headers=headers, data=postdata)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 0)
        filter = Mfilter(self)
        filter.run(data['data'], {
            'quantity|int|require',
            'currency_units|varchar|require'
        })

    '''选择支付页'''
    # def order_pay(self):
    #     lang=str(random.choice(1, 3))
    #     headers={}
    #     headers['Authorization']='bearer '+self.__get_user_token()
    #     headers['lang']=lang
    #     headers['currencycode']='sar'
    #     url='/api/order/pay?order_id='+





    def tearDown(self):
        pass



if __name__ == "__main__":
    unittest.main()
