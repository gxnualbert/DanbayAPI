#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: device.py
@time: 2017/12/26/14:52
"""
import unittest,requests


class aagetDeviceListAll(unittest.TestCase):
    def test_GetDeviceListAllWithCorrectInfo(self):
        host = 'http://test.www.danbay.cn/system'
        payload = {'mc_username': 'DBShow', 'mc_password': 'DBShow', 'ticket_consume_url': 'test.www.danbay.cn',
                   'return_url': 'www.baidu.com', 'random_code': 123456}
        r = requests.post(host + '/connect', data=payload)
        mtoken = r.url.split('mtoken=')[1]
        r = requests.post(host + '/deviceInfo/getDeviceIistAll?mtoken=%s' % mtoken)
        self.assertEquals(200, r.status_code)