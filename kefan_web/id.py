# _*_ coding:utf-8 _*_
import requests
import json
import time

# deviceid = "3FA3EF68-B6C7-4BD6-A0BE-E1D5B0A62DD9"
# appid = "1"
# catgId = "20"
# topDocKey = "fbTopDoc"
sleepSeconds = 4 #这个是请求间隔时间， 单位为秒。
times = 10 # 设置请求次数

# nsukey = "b7kWe5sGaHyUQRjKDvStaOpQjAg6YFiQW%2Fs4a%2BKwVM0h3pH60xO5xBRumGI78BvDEJPHJUKlbs%2BawOqQ%2B2yDmy0xKvTwq%2FmWN68qx02GugUAx1gtK5QSeVb0kvYGgP3TkLAGwTWX1bBygXg7MCQXtygcAjuYPPe0Fdla2k9iIr%2BcC16DTrzncllqmUE18gx%2FxUp7cQYQcPZpKNM5bDPIPA%3D%3D"
pageHtml = "http://47.91.93.147:17316/arabic/filter.do?appid=2&devid=642333e153271743&catgId=999&isNew=0&isNeed=0"
'''
http://47.91.93.147:17316/arabic/filter.do?appid=2&devid=642333e153271743&catgId=999&isNew=1&isNeed=0  下拉
http://47.91.93.147:17316/arabic/filter.do?appid=2&devid=642333e153271743&catgId=999&isNew=0&isNeed=0  上拉
'''
# 取出所有id
ids = []
for i in range(0,times):
    html = requests.get(pageHtml)
    jsonText = json.loads(html.text)
    print jsonText
    if "docs" in jsonText and len(jsonText["docs"]) > 0:
        for doc in jsonText["docs"]:
            ids.append(doc["id"])
    time.sleep(0)  # 这里是延迟设置

# 遍历整理
idDict = {}
for id in ids:
    if id in idDict.keys():
        idDict[id] += 1
    else:
        idDict[id] = 1
# 字典根据value排序
newIdDict = sorted(idDict.items(),key = lambda x:x[1],reverse = True)
if len(newIdDict) == len(ids):
    print("此次%d次请求无重复" % times)
else:
    print("请求有重复id，如下是详情\n")
    print(newIdDict)

