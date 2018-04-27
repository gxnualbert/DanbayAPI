#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: getToken.py
@time: 2017/12/26/11:48
"""

import requests
from readconf import ReadConfigFile
import json
class token():

    def LoginToken(self):
        configfile=ReadConfigFile()
        cf=configfile.getBasicConf()

        # host=cf["host"]
        # host="http://"+host+"/system/"
        username=cf["username"]
        password=cf["password"]
        url = cf["apiHostPrefix"]+"/connect"
        payload = {'mc_username':username, 'mc_password': password, 'ticket_consume_url':"www.baidu.com",
                   'return_url': 'www.baidu.com', 'random_code': 123456}
        r = requests.post(url, data=payload)
        tokenUrl=r.request.path_url

        # print r.status_code
        # print r.text
        # print tokenUrl.split('mtoken=')[1]
        # return r.url.split('mtoken=')[1]



    def getToken(self):
        configfile = ReadConfigFile()
        cf = configfile.getBasicConf()

        host = cf["host"]
        host = "http://" + host+"/system/"
        username = cf["username"]
        password = cf["password"]
        url = host + "/loginAccess"

        payload = {'mc_username': username, 'mc_password': password, 'ticket_consume_url': host,
                   'return_url': 'www.baidu.com', 'random_code': 123456}
        r = requests.post(url, data=payload)
        r = json.loads(r.text)
        token=r["result"]["mtoken"]
        return token


# a=token()
# # # # a.getToken2()
# a.LoginToken()