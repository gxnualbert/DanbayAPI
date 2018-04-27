#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:albert.chen
@file: lockUtil.py
@time: 2018/04/26/17:46
"""
import requests


class lockCommonUtil():
    def getCookies(self,username, password):
        loginurl = 'http://www.danbay.cn/system/goLoginning'
        payload = {'mc_username': username, 'mc_password': password, 'rememberMe': ""}
        r = requests.post(loginurl, data=payload)
        return r.cookies

    def lockSyncPwd(self,deviceID,username,password):
        reqUrl="http://test.www.danbay.cn/system/lock/socket/getPwdInfo?deviceId="+deviceID
        r = requests.post(reqUrl,  cookies=self.getCookies(username,password))





