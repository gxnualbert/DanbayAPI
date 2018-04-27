#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
@author:albert.chen
@file: test.py
@time: 2017/12/12/13:02
"""

import requests,json
#
#
# # payload={"text":"推送标题","desp":"推送内容：sendkey不再payload中的\r 测试换行"}
# payload={"text":"推送标题","desp":"##1、测试\n#2json格式"}
# r=requests.post(url="https://pushbear.ftqq.com/sub?sendkey=1709-bdb1ea4ce8e26859177df1602ed5008b",data=payload)
#
# print r.text

def getDeviceListAllWithCorrectInfo():
    local_filename="export.csv"
    r=requests.get("http://www.danbay.cn/system/engeryDevice/exportConsumptionCount?type=1&beginTime=2017-12-01&endTime=2017-12-26&houseInfoIds=10048_10026_9629",stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    # print r.text
    # host = 'http://test.www.danbay.cn/system/goLoginning'
    # payload = {'mc_username': 'admin', 'mc_password': 'dbadmin$666', 'rememberMe':""}
    # r = requests.post(host ,data=payload)
    # print r.cookies
    #
    # getEnergyDeviceBatch="http://test.www.danbay.cn/system/engeryDevice/getEnergyDeviceBatch"
    #
    # payload={"type":"1","beginTime":"2017-12-01","endTime":"2017-12-26","houseInfoIds":"6700"}
    # mtoken = r.url.split('mtoken=')[1]
    # r = requests.post(host + '/deviceInfo/getDeviceIistAll?mtoken=%s' % mtoken)
    # # print r.text
    # rsp=json.loads(r.text)
    # rsp=rsp["result"]
    # for i in rsp:
    #     print i["deviceId"],i["deviceType"]

getDeviceListAllWithCorrectInfo()