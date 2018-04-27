#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: test_GetToken.py
@time: 2017/12/18/20:53
"""
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import unittest,requests
import time

# from Util import CheckReportDir as checkDir
# from Util.HTMLTestRunner import HTMLTestRunner
class TestIni(unittest.TestCase):
    def setUp(self):
        print "test case start"
        # 读取配置文件，一些公共的信息，比如host
    def tearDown(self):
        print "test case end"


class test_GetToken(unittest.TestCase):
    host='http://test.www.danbay.cn/system'
    def test_GetTokenWithCorrectInfo(self):
        self.url=self.host+'/connect'
        payload = {'mc_username': 'DBShow', 'mc_password': 'DBShow', 'ticket_consume_url': 'test.www.danbay.cn',
                   'return_url': 'www.baidu.com', 'random_code': 123456}
        r = requests.post(self.host + '/connect', data=payload)
        self.assertEquals(200,r.status_code)
    def test_GetTokenWithWrongInfo(self):
        self.url = self.host + '/connect'
        payload = {'mc_username': 'DBShow', 'mc_password': 'DBShow', 'ticket_consume_url': 'test.www.danbay.cn',
                   'return_url': 'www.baidu.com', 'random_code': 123456}
        r = requests.post(self.host + '/connect', data=payload)
        mtoekn = r.url.split('mtoken=')[1]









# if __name__=="__main__":
#
#
#     suite = unittest.TestSuite()
#     suite.addTest(test_GetToken("test_GetTokenWithCorrectInfo"))
#
#     now=time.strftime("%Y-%m-%d %H_%M_%S")
#     reportPath=checkDir.CheckReportPath.getReportPath()
#     filename="蛋贝云端智能服务系统接口测试报告"+now+".html"
#     reportFile=reportPath+"\\\\"+filename
#     fp=open(reportFile.decode('utf-8'), "wb")
#     runner=HTMLTestRunner(stream=fp,title="蛋贝云端智能服务系统接口测试报告",description="蛋贝云端智能服务系统接口测试报告")
#     runner.run(suite)
#     fp.close()