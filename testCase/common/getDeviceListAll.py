#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: test_getDeviceListAll.py
@time: 2017/12/26/10:56
"""

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import unittest,requests
from Util.readconf import ReadConfigFile
from Util.getToken import token


class getDeviceListAll(unittest.TestCase):

    def test_getDeviceListAllWithCorrectInfo(self):

        configfile=ReadConfigFile()
        apiHostPrefix=configfile.getBasicConf()["apiHostPrefix"]

        tk=token()
        mtoken=tk.getToken()

        r = requests.post(apiHostPrefix + '/deviceInfo/getDeviceIistAll?mtoken=%s' % mtoken)
        self.assertEquals(200, r.status_code)



