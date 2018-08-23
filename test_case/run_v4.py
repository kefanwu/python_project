# _*_ coding:utf-8 _*_

__author__ = 'chenhuan'

import unittest
import sys
import requests
import ConfigParser
import os
import json
reload(sys)
sys.setdefaultencoding("utf-8")


class Run(unittest.TestCase):
    def setUp(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.abspath('.')+'/env.conf')
        self.conf = conf
        self.base_url = conf.get("env", "host")
        self.app_name = conf.get("env", "app_name")
        self.device_id = conf.get("app", "user_device_id")

        self.headers = {
            'Access-Token': self.device_id,
            'Accept': 'application/vnd.' + self.app_name + '.v4+json'
        }


    '''文章分类'''
    def article_categories(self):
        response = requests.get(self.base_url+"/ar_AE/api/article_categories" ,headers = self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['code'], 1)
        self.assertNotEqual(json.loads(response.content)['content'], [])

    '''视频分类'''
    def video_categories(self):
        response = requests.get(self.base_url + "/ar_AE/api/video_categories", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['code'], 1)
        self.assertNotEqual(json.loads(response.content)['content'], [])


    '''文章列表'''
    def article_list(self):

        category_id = self.conf.get('app','test_article_category_id')
        response = requests.get(self.base_url+"/ar_AE/api/article_list_v2/"+category_id+"/0" ,headers = self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['code'], 1)
        self.assertNotEqual(json.loads(response.content)['content'], [])

    '''视频列表'''
    def video_list(self):
        category_id = self.conf.get('app','test_video_category_id')
        response = requests.get(self.base_url+"/ar_AE/api/video_list/"+category_id ,headers = self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['code'], 1)
        self.assertNotEqual(json.loads(response.content)['content'], [])

    '''推荐新接口'''
    def recommend(self):
        response = requests.get(self.base_url+"/ar_AE/api/recommend/0" ,headers = self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['code'], 1)
        self.assertNotEqual(json.loads(response.content)['content'], [])


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
