# _*_ coding:utf-8 _*_
'''
__author__ = 'wukefan'
'''


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
            'Access-Token':self.device_id,
            'Accept': 'application/vnd.' + self.app_name + '.v3+json'
        }

    '''测试服推荐页取文章创建时间，ID,posttype'''
    def recommend(self):
        url = "http://api.test.wekoora.com/ar_AE/api/recommend/"
        # has = []
        # not_has = []
        for i in range(0, 25):
            page = i * 10
            response = requests.get(url+str(page),headers = self.headers)
            # print response.content
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content)['code'], 1)
            self.assertNotEqual(json.loads(response.content)['content']['recommend']['data'], [])
            content= json.loads(response.content)['content']['recommend']['data']
            for item in content:
                created_at = item['created_at']
                id = item['id']
                posttype = item['posttype']
                print created_at,id,posttype
                # if created_at and id and posttype != None:
                #     has.append(created_at,id,posttype)
                # else:
                #     not_has.append(created_at,id,posttype)
                # if len(has)>0:
                #     self.assertEqual(json.dumps(has),-1)






    '''视频列表'''
    def video_list(self):
        category_id = self.conf.get('app','test_video_category_id')
        response = requests.get(self.base_url+"/ar_AE/api/video_list/"+category_id ,headers = self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['code'], 1)
        self.assertNotEqual(json.loads(response.content)['content'], [])

    '''详情'''
    def article_details(self):
        test_id = self.conf.get('app','test_id')
        response = requests.get(self.base_url+"/ar_AE/api/article_details/"+test_id ,headers = self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['code'], 1)
        self.assertNotEqual(json.loads(response.content)['content'], [])



    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
