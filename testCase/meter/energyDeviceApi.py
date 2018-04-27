#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:albert.chen
@file: energyDeviceApi.py
@time: 2018/04/24/9:51
"""

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import unittest,requests
import json
from Util.readconf import ReadConfigFile
from Util.getToken import token

class getEnergyDeviceApi(unittest.TestCase):

    # def __init__(self, name):
    #     configfile = ReadConfigFile()
    #     self.apiHostPrefix = configfile.getBasicConf()["apiHostPrefix"]
    #     self.tk = token()
    #     self.mtoken = self.tk.getToken()
    configfile = ReadConfigFile()
    apiHostPrefix = configfile.getBasicConf()["apiHostPrefix"]

    tk = token()
    mtoken = tk.getToken()

    def test_getEnergyDeviceList(self):
        r = requests.post(self.apiHostPrefix + '/deviceInfo/getEnergyDeviceList?mtoken=%s' % self.mtoken)
        self.assertEquals(200, r.status_code,msg=u"状态码不等于200")

    def test_getEnergyDeviceInfo(self):
        # 需要从文件列表中读取设备id （水电表各一个？？？）
        r = requests.post(self.apiHostPrefix + '/deviceInfo/getEnergyDeviceInfo?deviceId=%s&mtoken=%s' %("",self.mtoken))
        self.assertEquals(200, r.status_code)

    def test_getEnergyDailyReading(self):
        # 从log_report中获取某一天的读数，然后跟api中的读数对比
        r = requests.post(
            self.apiHostPrefix + '/deviceInfo/getEnergyDailyReading?deviceId=%s&readTime=%s&mtoken=%s' % ("", "readtime",self.mtoken))
        self.assertEquals(200, r.status_code)

    def test_getEnergySectionConsumption(self):
        # 从log report中获取某几天的读数，然后跟API中的读数对比
        r = requests.post(
            self.apiHostPrefix + '/deviceInfo/getEnergySectionConsumption?deviceId=%s&startTime=%s&endTime=%s&mtoken=%s'% (
            "deviceId","startTime" "endTime", self.mtoken))
        self.assertEquals(200, r.status_code)

    def test_energy_gateControl(self):
        r = requests.post(
            self.apiHostPrefix + '/deviceInfo/energy/gateControl?deviceId=%s&startTime=%s&endTime=%s&mtoken=%s' % (
                "deviceId", "startTime" "endTime", self.mtoken))
        self.assertEquals(200, r.status_code)

    def test_energy_getGateStatus(self):
        r = requests.post(
            self.apiHostPrefix + '/deviceInfo/energy/getGateStatus?deviceId=%s&mtoken=%s' % (
                "deviceId",  self.mtoken))
        self.assertEquals(200, r.status_code)

    # def test_