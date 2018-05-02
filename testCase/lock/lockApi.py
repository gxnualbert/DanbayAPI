#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: test_getLockList.py
@time: 2017/12/26/11:36
"""

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import unittest,requests
import json
import datetime
from Util.readconf import ReadConfigFile
from Util.getToken import token
from Util.dboperation import dbOperate
from Util.lockUtil import lockCommonUtil
import time
from Util.logTool import AddLog as log

class getLockApi(unittest.TestCase):

    configfile = ReadConfigFile()

    #配置文件信息部分
    apiHostPrefix = configfile.getBasicConf()["apiHostPrefix"]
    username=configfile.getBasicConf()["username"]
    password=configfile.getBasicConf()["password"]
    lockDeviceID=configfile.getLockInfo()["lockDeviceID"]
    lockPwd_addPwd_zuke=configfile.getLockInfo()["lockPwd_addPwd_zuke"]
    lockPwd_addPwd_tmp = configfile.getLockInfo()["lockPwd_addPwd_tmp"]  # 添加的租客密码
    lockPwd_addPwd_gj = configfile.getLockInfo()["lockPwd_addPwd_gj"]  # 添加的租客密码
    lockPwd_addPwdWithDate_zuke = configfile.getLockInfo()["lockPwd_addPwdWithDate_zuke"]  # 添加的租客密码
    lockPwd_editPwd_zuke = configfile.getLockInfo()["lockPwd_editPwd_zuke"]  # 添加的租客密码
    lockPwd_editPwd_gj = configfile.getLockInfo()["lockPwd_editPwd_gj"]  # 添加的租客密码



    # 测试用例使用的全局变量
    reportTime = datetime.datetime.now().strftime("%Y-%m-%d") #过滤日志使用的时间，精确到天
    allPwdAddTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    allPwdAddTime = allPwdAddTime[2:]   #门锁添加密码的时间，不论什么密码，检查时间都从这个时间开始，这样后面每个测试用例就不用单独添加时间

    # 门锁密码ID和别名
    lockPwd_addPwd_zuke_pwdID=""
    lockPwd_addPwd_zuke_pwdID_Alias =""
    lockPwd_addPwd_tmp_pwdID=""
    lockPwd_addPwd_tmp_pwdID_Alias =""
    lockPwd_addPwd_gj_pwdID=""
    lockPwd_addPwd_gj_pwdID_Alias=""
    lockPwd_addPwdWithDate_zuke_pwdID=""

    #其他工具实例化
    lockTool=lockCommonUtil()
    tk = token()
    mtoken = tk.getToken()

    #API URL路径
    deviceInfo="/deviceInfo/"
    deviceCtrllockPwd="/deviceCtrl/lockPwd/"
    db=dbOperate()

    def test_getLockList_StatusCode(self):
        r = requests.post(self.apiHostPrefix +self.deviceInfo+ 'getLockList?mtoken=%s' %self.mtoken)
        self.assertEquals(200, r.status_code, msg=u'返回的状态码不等于200')
    def test_getLockList_Message(self):
        r = requests.post(self.apiHostPrefix + self.deviceInfo+'getLockList?mtoken=%s' % self.mtoken)
        rsp = json.loads(r.text)
        message=rsp["message"]
        self.assertEquals(u"查询成功", message,msg=u'message不等于提示信息 查询成功 ')
    def test_getLockList_DeviceID(self):
        '比较配置文件中实际的deviceid 跟api返回来的deviceid'
        r = requests.post(self.apiHostPrefix + self.deviceInfo+'getLockList?mtoken=%s' % self.mtoken)
        rsp = json.loads(r.text)
        result=rsp["result"]
        result=result[0]
        deviceid=result['deviceId']
        self.assertEquals(self.lockDeviceID, deviceid, msg=u'API 返回的门锁设备id:%s 不等于实际门锁的设备id：%s'%(deviceid,self.lockDeviceID))
    def test_getLockInfo_Message(self):
        r = requests.post(self.apiHostPrefix + self.deviceInfo+'getLockInfo?deviceId=%s&mtoken=%s' % (self.lockDeviceID,self.mtoken))
        self.assertEquals(200, r.status_code)
        rsp = json.loads(r.text)
        message = rsp["message"]
        self.assertEquals(u"查询成功", message, msg=u'message不等于提示信息 查询成功 ')
    def test_getLockInfo_StatusCode(self):
        r = requests.post(self.apiHostPrefix + self.deviceInfo+'getLockInfo?deviceId=%s&mtoken=%s' % (self.lockDeviceID,self.mtoken))
        self.assertEquals(200, r.status_code)
    def test_getLockInfo_Message(self):
        r = requests.post(self.apiHostPrefix + self.deviceInfo + 'getLockInfo?deviceId=%s&mtoken=%s' % (
        self.lockDeviceID, self.mtoken))
        rsp = json.loads(r.text)
        message = rsp["result"]
        self.assertEquals(u"查询成功", message, msg=u'message不等于提示信息 查询成功 ')
    def test_getLockInfo_OnlineStatus(self):

        r = requests.post(self.apiHostPrefix + self.deviceInfo+'getLockInfo?deviceId=%s&mtoken=%s' % (
            self.lockDeviceID, self.mtoken))
        rsp = json.loads(r.text)
        message = rsp["result"]
        LockStatus=message["deviceStatus"]
        lockOnlineStatusSql="SELECT online FROM device_info WHERE deviceId="+ "\'" +self.lockDeviceID+"\'"
        queryResult=self.db.dbOperation(lockOnlineStatusSql)
        # 0 在线 1 离线
        self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')
        self.assertEquals(int(LockStatus), int(queryResult[0][0]), msg=u'门锁的在线状态跟数据的不一致，API返回门锁的是%s,数据库中查到的是%s,其中，0表示在线，1表示离线 '%(LockStatus,queryResult[0][0]))
    def test_deviceCtrl_lockPwd_addPwd_zuke(self):
        '''
        根据范爷跟张建反馈，后续31,51,06,04Pro都只有一个管家密码
        之前5个管家密码，主要是由warm家那边提出来的，5个管家密码的锁有：03,04,05这3把锁
        因此，这里添加管家密码，就不做测试
        :return:
        '''
        r = requests.post(self.apiHostPrefix + self.deviceCtrllockPwd + 'addPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s' % (self.lockDeviceID,self.lockPwd_addPwd_zuke,"3", self.mtoken))
        rsp = json.loads(r.text)
        getLockApi.lockPwd_addPwd_zuke_pwdID=rsp["result"]["pwdID"]
        self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')
        addPwd_zuke_pwdAliasSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(getLockApi.lockPwd_addPwd_zuke_pwdID) + "\'"
        addPwd_zuke_pwdAlias = self.db.dbOperation(addPwd_zuke_pwdAliasSql)
        addPwd_zuke_pwdAlias = addPwd_zuke_pwdAlias[0][0]
        log.Log("下发新增租客密码指令成功！！！租客密码为%s，API返回的状态码为：%s,密码别名为：%s" % (self.lockPwd_addPwd_zuke, r.status_code, addPwd_zuke_pwdAlias))
        getLockApi.lockPwd_addPwd_zuke_pwdID_Alias = addPwd_zuke_pwdAlias
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,addPwd_zuke_pwdAlias, 3)
        log.Log("新增租客密码权限动态已经校验完成！！！查找结果为：%s(备注：0 没找到，1 找到)。权限动态列表为：%s,findResult。"%(findResult[0],findResult[1]))
        self.assertEquals(1, findResult[0], msg=u'无权限动态上报。检查权限动态列表为：%s' % (findResult[1]))
    def test_deviceCtrl_lockPwd_addPwdWithDate_zuke(self):
        d1=datetime.datetime.now()
        d3=d1.strftime("%Y-%m-%d %H:%M:%S")
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'addPwdWithDate?deviceId=%s&password=%s&pwdType=%s&mtoken=%s&beginTime=%s&endTime=%s' % (
                self.lockDeviceID, self.lockPwd_addPwdWithDate_zuke, "3", self.mtoken,d3,d1 + datetime.timedelta(hours=1)))
        rsp = json.loads(r.text)
        getLockApi.lockPwd_addPwdWithDate_zuke_pwdID = rsp["result"]["pwdID"]
        self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')
        withDate_zuke_pwdAliasSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(getLockApi.lockPwd_addPwdWithDate_zuke_pwdID) + "\'"
        withDate_zuke_db_pwdAlias = self.db.dbOperation(withDate_zuke_pwdAliasSql)
        withDate_zuke_db_pwdAlias = withDate_zuke_db_pwdAlias[0][0]
        log.Log("添加指定时效的租客密码为%s，密码别名为：%s，状态码为：%s。密码开始时间：%s,密码结束时间:%s" % (
        self.lockPwd_addPwdWithDate_zuke,withDate_zuke_db_pwdAlias , r.status_code,d3,(d1 + datetime.timedelta(hours=1))))
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,withDate_zuke_db_pwdAlias, 3)
        self.assertEquals(1, findResult[0], msg=u'无权限动态上报。调用API新增密码时间%s，检查权限动态列表为：%s' % (d3, findResult[1]))

    def test_deviceCtrl_lockPwd_addPwd_tmp(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'addPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s' % (
                self.lockDeviceID, self.lockPwd_addPwd_tmp, "0", self.mtoken))
        rsp = json.loads(r.text)

        getLockApi.lockPwd_addPwd_tmp_pwdID =rsp["result"]["pwdID"]
        self.assertEquals(200, r.status_code, msg=u'添加临时密码API返回的状态码不等于200')

        addPwd_tmp_pwdIDSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(getLockApi.lockPwd_addPwd_tmp_pwdID) + "\'"
        tmp_db_pwdAlias = self.db.dbOperation(addPwd_tmp_pwdIDSql)
        tmp_db_pwdAlias = tmp_db_pwdAlias[0][0]
        getLockApi.lockPwd_addPwd_tmp_pwdID_Alias=tmp_db_pwdAlias
        log.Log("添加临时密码为%s，密码别名为：%s，状态码为：%s。" % (
            self.lockPwd_addPwd_tmp, tmp_db_pwdAlias, r.status_code))
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         tmp_db_pwdAlias, 0)
        self.assertEquals(1, findResult[0], msg=u'无权限动态上报。检查权限动态列表为：%s' % (findResult[1]))
        log.Log("权限动态列表：%s" % (findResult[1]))
    def test_deviceCtrl_lockPwd_addPwd_gj(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'addPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s' % (
                self.lockDeviceID, self.lockPwd_addPwd_gj, "2", self.mtoken))
        rsp = json.loads(r.text)
        lock_gj_addTime= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        getLockApi.lockPwd_addPwd_gj_pwdID = rsp["result"]["pwdID"]
        log.Log("添加管家密码：%s，密码编号pwdID为：%s，返回的状态码为：%s" % (self.lockPwd_addPwd_gj, getLockApi.lockPwd_addPwd_gj_pwdID,r.status_code))
        self.assertEquals(200, r.status_code, msg=u'添加管家密码API返回的状态码不等于200')

        pwdIDSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(
            getLockApi.lockPwd_addPwd_gj_pwdID) + "\'"
        db_pwdAlias = self.db.dbOperation(pwdIDSql)
        db_pwdAlias = db_pwdAlias[0][0]
        getLockApi.lockPwd_addPwd_gj_pwdID_Alias=db_pwdAlias
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         db_pwdAlias, "addPwd_gj")
        log.Log("权限动态列表为：%s"%findResult[1])
        self.assertEquals(1, findResult[0], msg=u'新增管家密码后，没有收到权限动态上报，就发送密码出来了。调用API新增管家密码时间%s，检查权限动态列表为：%s' % (
            lock_gj_addTime, findResult[1]))
    def test_deviceCtrl_lockPwd_editPwd_zuke(self):
        r = requests.post(self.apiHostPrefix + self.deviceCtrllockPwd + 'editPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s&pwdID=%s' % (self.lockDeviceID, self.lockPwd_editPwd_zuke, "3", self.mtoken,getLockApi.lockPwd_addPwd_zuke_pwdID))
        self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')
        editPwd_zuKepwdAliasSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(getLockApi.lockPwd_addPwd_zuke_pwdID) + "\'"
        editPwd_zuKe_db_pwdAlias = self.db.dbOperation(editPwd_zuKepwdAliasSql)
        editPwd_zuKe_db_pwdAlias = editPwd_zuKe_db_pwdAlias[0][0]
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,editPwd_zuKe_db_pwdAlias, 4)
        log.Log("新修改后的租客密码是：%s,密码别名是：%s,权限动态列表为：%s" % (self.lockPwd_editPwd_zuke,editPwd_zuKe_db_pwdAlias,findResult[1]))
        self.assertEquals(1, findResult[0], msg=u'检查权限动态列表为：%s' % ( findResult[1]))
    def test_deviceCtrl_lockPwd_editPwd_gj(self):
        # 注意，选择管家密码的时候，要区分状态status 0，正常，4，操作中
        # 默认管家密码都可以新增，后续不能新增，在去修改原来固定的密码
        r = requests.post(self.apiHostPrefix + self.deviceCtrllockPwd + 'editPwd?deviceId=%s&password=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (self.lockDeviceID, self.lockPwd_addPwd_gj_pwdID, "2", getLockApi.lockPwd_editPwd_gj_pwdID, self.mtoken))
        self.assertEquals(200, r.status_code, msg=u'修改管家密码API返回的状态码不等于200')
        editPwd_gj_pwdAliasSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(getLockApi.lockPwd_addPwd_gj_pwdID) + "\'"
        editPwd_gj_db_pwdAlias = self.db.dbOperation(editPwd_gj_pwdAliasSql)
        editPwd_gj_db_pwdAlias = editPwd_gj_db_pwdAlias[0][0]
        log.Log("修改管家密码指令发送成功，新修改后的管家密码是：%s，别名是：%s" % (self.lockPwd_addPwd_gj_pwdID,getLockApi.lockPwd_addPwd_gj_pwdID_Alias))
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,editPwd_gj_db_pwdAlias, 5)
        log.Log("权限动态列表是：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'修改管家密码后，无权限动态上报。检查权限动态列表为：%s' % (
             findResult[1]))
    def test_deviceCtrl_lockPwd_updatePwd_freeze_zuke(self):
        # 这里先假设前面的密码都已经成功加进去了。异常情况，后面再处理。针对异常情况，后面可以通过全局性的标志来决定改用例是否能被执行
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "0","3", getLockApi.lockPwd_addPwd_zuke_pwdID, self.mtoken))
        log.Log("冻结租客密码指令发送成功，冻结的租客pwdID是：%s" % getLockApi.lockPwd_addPwd_zuke_pwdID)
        updatePwd_stop_zuKe_time=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'冻结租客密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockPwd_addPwd_zuke_pwdID_Alias, "updatePwd_freeze_zuke")
        log.Log("查找的权限动态列表：%s"%findResult[1])
        self.assertEquals(1, findResult[0], msg=u'冻结租客密码后，没有收到权限动态上报。调用API冻结密码时间%s，检查权限动态列表为：%s' % (
            updatePwd_stop_zuKe_time, findResult[1]))
    def test_deviceCtrl_lockPwd_updatePwd_unfreeze_zuke(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "1", "3", getLockApi.lockPwd_addPwd_zuke_pwdID, self.mtoken))
        log.Log("解冻租客密码指令发送成功，解冻的租客密码别名是：%s" % getLockApi.lockPwd_addPwd_zuke_pwdID_Alias)
        updatePwd_unstop_zuKe_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'冻结租客密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockPwd_addPwd_zuke_pwdID_Alias, "updatePwd_unfreeze_zuke")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'解冻租客密码后，没有收到权限动态上报。调用API解冻密码时间%s，检查权限动态列表为：%s' % (
            updatePwd_unstop_zuKe_time, findResult[1]))
    def test_deviceCtrl_lockPwd_updatePwd_freeze_gj(self):
        # 这里先假设前面的密码都已经成功加进去了。异常情况，后面再处理。针对异常情况，后面可以通过全局性的标志来决定改用例是否能被执行
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "0", "2", getLockApi.lockPwd_addPwd_gj_pwdID, self.mtoken))
        log.Log("冻结管家密码指令发送成功，冻结的管家别名是：%s" % getLockApi.lockPwd_addPwd_gj_pwdID_Alias)
        updatePwd_stop_gj_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'冻结管家密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockPwd_addPwd_gj_pwdID_Alias, "updatePwd_freeze_gj")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'冻结管家密码后，没有收到权限动态上报。调用API冻结密码时间%s，检查权限动态列表为：%s' % (
            updatePwd_stop_gj_time, findResult[1]))
    def test_deviceCtrl_lockPwd_updatePwd_unfreeze_gj(self):
        # 这里先假设前面的密码都已经成功加进去了。异常情况，后面再处理。针对异常情况，后面可以通过全局性的标志来决定改用例是否能被执行
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "1", "2", getLockApi.lockPwd_addPwd_gj_pwdID, self.mtoken))
        log.Log("解冻管家密码指令发送成功，解冻的管家别名是：%s" % getLockApi.lockPwd_addPwd_gj_pwdID_Alias)
        updatePwd_unstop_gj_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'解冻管家密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockPwd_addPwd_gj_pwdID_Alias, "updatePwd_unfreeze_gj")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'解冻管家密码后，没有收到权限动态上报。调用API解冻管家密码时间%s，检查权限动态列表为：%s' % (
            updatePwd_unstop_gj_time, findResult[1]))
    def test_deviceCtrl_lockPwd_delPwd_zuke(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'delPwd?deviceId=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "3",getLockApi.lockPwd_addPwd_zuke_pwdID , self.mtoken))
        log.Log("删除租客密码指令发送成功，删除的租客密码别名是：%s" % getLockApi.lockPwd_addPwd_zuke_pwdID_Alias)
        updatePwd_stop_zuKe_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'删除租客密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockPwd_addPwd_zuke_pwdID_Alias, "delPwd_zuke")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'删除租客密码后，没有收到权限动态上报。调用API冻结密码时间%s，' % (
            updatePwd_stop_zuKe_time))
    def test_deviceCtrl_lockPwd_delPwd_tmp(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'delPwd?deviceId=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "0", getLockApi.lockPwd_addPwd_tmp_pwdID, self.mtoken))
        log.Log("删除的临时密码的别名是：%s，API返回的状态码是：%s" % (getLockApi.lockPwd_addPwd_tmp_pwdID_Alias,r.status_code))
        updatePwd_stop_zuKe_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'删除临时密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockPwd_addPwd_tmp_pwdID_Alias, "delPwd_tmp")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'删除租客密码后，没有收到权限动态上报。调用API冻结密码时间%s，' % (
            updatePwd_stop_zuKe_time))
    def test_deviceCtrl_lockPwd_delPwd_gj(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'delPwd?deviceId=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "2", getLockApi.lockPwd_addPwd_gj_pwdID, self.mtoken))
        log.Log("删除管家密码指令发送成功，删除的管家密码的别名是：%s，API返回的状态码是：%s" % (getLockApi.lockPwd_addPwd_gj_pwdID_Alias, r.status_code))
        del_gj_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'删除管家密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockPwd_addPwd_gj_pwdID_Alias, "delPwd_gj")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'删除管家密码后，没有收到权限动态上报。调用API删除密码时间%s，' % (
            del_gj_time))




# a=getLockApi()
# a.test_getLockList()
# a=getLockList()
# a.test_getDeviceListAllWithCorrectInfo()