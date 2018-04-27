#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:albert.chen
@file: checkToken.py
@time: 2018/04/24/15:14
"""

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import unittest,requests
from Util.readconf import ReadConfigFile

class connect(unittest.TestCase):

    configfile = ReadConfigFile()
    apiHostPrefix = configfile.getBasicConf()["apiHostPrefix"]
    username = configfile.getBasicConf()["username"]
    password = configfile.getBasicConf()["password"]
    url = configfile.getBasicConf()["apiHostPrefix"] + "/connect"
    validTokenUrl=configfile.getBasicConf()["apiHostPrefix"] + "/deviceInfo/getDeviceListAll"

    '''
    针对API中的第二种获取token的方法，因为后续所有的请求都是根据第二种方式来获取token的，所以，这里
    就不在测第二种获取token的方法了！！！！！！！！！
    '''
    def test_connect(self):
        payload = {'mc_username': self.username, 'mc_password': self.password, 'ticket_consume_url': "www.baidu.com",
                   'return_url': 'www.baidu.com', 'random_code': 123456}
        r = requests.post(self.url, data=payload)

        self.assertEquals(200,r.status_code,"获取token时返回的状态码")

        # 根据获取到的token，拿某一个设备id
        tokenUrl = r.request.path_url
        accessToken=tokenUrl.split('mtoken=')[1]
        validTokenRsp = requests.post(self.validTokenUrl+'?mtoken=%s' % accessToken)

        self.assertEquals(200,validTokenRsp.status_code,msg=u"校验上一步中通过接口connect拿到的状态码")



