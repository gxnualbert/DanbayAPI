#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: test_GetLockList.py
@time: 2017/12/18/23:50
"""

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import unittest,requests

class test_GetLockList(unittest.TestCase):

    def test_GetLockListWithCorrectInfo(self):
        host = 'http://test.www.danbay.cn/system'
        payload = {'mc_username': 'DBShow', 'mc_password': 'DBShow', 'ticket_consume_url': 'test.www.danbay.cn',
                   'return_url': 'www.baidu.com', 'random_code': 123456}
        r = requests.post(host + '/connect', data=payload)
        mtoken = r.url.split('mtoken=')[1]
        r = requests.post(host + '/deviceInfo/getLockIist?mtoken=%s' % mtoken)
        self.assertEquals (200,r.status_code)