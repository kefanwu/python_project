# -*- coding: UTF-8 -*-
import requests
import json

response = requests.get("http://47.91.65.163:17710/focus/search.do?appType=fbAndroid&version=1.3.92&devid=642333e153271743""&focusType=member&focusId=99999999&isNew=1&isNeed=1")
data = json.loads(response.content)

# if data['docs']==None:
#     print "has New is 0"
#     exit(0)

content =data['docs']

for item in content:
    title =item['title']
    id = item['id']
    print (id)

    if title.find(u"الأهلي")>0:
        print ("title有关键词")
    else:
        print (u"title不包含关键词")
        headers= {'Access-Token':'642333e153271743'}
        url = "http://api.wekoora.com/ar_AE/api/article_details/"+id
        for i in range(10):
            response=requests.get(url,None,headers=headers)
            content = json.loads(response.content)
            print (content)
        # acticle=content ['content']['content']
        # if acticle.find(u"الأهلي") > 0:
        #     print u"acticle有关键词"
        # else:
        #     print u"acticle不包含关键词"



import requests

url = 'http://www.baidu.com.cn/'

fout = open('result.txt', 'w')

for i in range(10):
    r = requests.post(url)

    fout.write(url + ' ： OK withstatus_code: ' + str(r.status_code))

    print(url + ' ： OK withstatus_code: ' + str(r.status_code))

fout.close()