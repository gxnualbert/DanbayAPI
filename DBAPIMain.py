#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: DBAPIMain.py
@time: 2017/12/11/20:28
"""
import unittest
import time
import datetime
from Util import CheckReportDir as checkDir
from Util.HTMLTestRunner import HTMLTestRunner
from testCase import test_GetToken,test_GetDeviceListAll,test_GetLockList
# from testCase.common.getDeviceListAll import aagetDeviceListAll
# from testCase.test_device import test_aagetDeviceListAll
# from testCase.common.getDeviceListAll import getDeviceListAll
from testCase.dbdevice.deviceApi import getDeviceListAll
from testCase.lock.lockApi import getLockApi
from testCase.meter.energyDeviceApi import getEnergyDeviceApi
from testCase.validtoken.checkToken import connect
# from testCase import device

suite = unittest.TestSuite()

# suite.addTest(getLockApi("test_getLockList_Statuscode"))
# suite.addTest(getLockApi("test_getLockList_Message"))
# suite.addTest(getLockApi("test_getLockList_DeviceID"))
# suite.addTest(getLockApi("test_getLockInfo_Message"))
# suite.addTest(getLockApi("test_getLockInfo_OnlineStatus"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_addPwd_zuKe_StatusCode"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_addPwd_zuKe_CheckStatusAccess"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_addPwdWithDate_zuKe_StatusCode"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_addPwdWithDate_zuKe_CheckStatusAccess"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_addPwd_tmp_StatusCode"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_addPwd_tmp_CheckStatusAccess"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_editPwd_zuKe_StatusCode"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_editPwd_zuKe_CheckStatusAccess"))
# suite.addTest(getLockApi("test_deviceCtrl_lockPwd_editPwd_gj_StatusCode"))
# suite.addTest(getLockApi("test_deviceCtrl_lockPwd_editPwd_gj_CheckStatusAccess"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_updatePwd_stop_zuKe"))
suite.addTest(getLockApi("test_deviceCtrl_lockPwd_delPwd_zuKe"))



# suite.addTest(getLockApi("test_deviceCtrl_lockPwd_addPwd_zuKe_StatusCode"))
# suite.addTest(getLockApi("test_getLockInfo"))
# suite.addTest(getEnergyDeviceApi("test_getEnergyDeviceList"))
# suite.addTest(connect("test_connect"))
# suite.addTest(getDeviceListAll("test_getDeviceListAll"))


if __name__=="__main__":

    now=time.strftime("%Y-%m-%d %H_%M_%S")
    startTime = datetime.datetime.now()
    print "开始时间：",time.strftime("%Y-%m-%d %H:%M:%S")
    reportPath=checkDir.CheckReportPath.getReportPath()
    filename="蛋贝云端智能服务系统接口测试报告"+now+".html"
    reportFile=reportPath+"\\\\"+filename
    fp=open(reportFile.decode('utf-8'), "wb")
    runner=HTMLTestRunner(stream=fp,title="蛋贝云端智能服务系统接口测试报告",description="蛋贝云端智能服务系统接口测试报告")
    runner.run(suite)
    fp.close()

    end=time.strftime("%Y-%m-%d %H:%M:%S")
    endtime  = datetime.datetime.now()
    print "\n"
    print "结束时间：",end

    print u"总共花费时间为: %s" % (endtime - startTime)
