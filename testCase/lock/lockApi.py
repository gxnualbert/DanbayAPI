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
# class test_getDeviceListAll(unittest.TestCase):

class getLockApi(unittest.TestCase):

    configfile = ReadConfigFile()

    #配置文件信息部分
    apiHostPrefix = configfile.getBasicConf()["apiHostPrefix"]
    username=configfile.getBasicConf()["username"]
    password=configfile.getBasicConf()["password"]
    lockDeviceID=configfile.getLockInfo()["lockDeviceID"]
    lockNewAddZuKePwd=configfile.getLockInfo()["lockNewAddZuKePwd"]
    lockPwd_addPwd_Tmp = configfile.getLockInfo()["lockPwd_addPwd_Tmp"]  # 添加的租客密码
    lockPwd_addPwdWithDate = configfile.getLockInfo()["lockPwd_addPwdWithDate"]  # 添加的租客密码



    #
    lockNewAddZuKePwd_pwdID=""
    lockNewAddZuKePwd_Alias =""
    lock_gj_alias=""

    # 测试用例使用的全局变量
    reportTime = datetime.datetime.now().strftime("%Y-%m-%d") #过滤日志使用的时间，精确到天

    allPwdAddTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    allPwdAddTime = allPwdAddTime[2:]   #门锁添加密码的时间，不论什么密码，检查时间都从这个时间开始，这样后面每个测试用例就不用单独添加时间

    zuKePwdAddTime=""#无指定时效的密码的添加时间记录
    zuKePwdAddTimeWithDate=""

    addPwdWithDate_pwdID=""#

    addPwdWithDate_AddTime=""# 制定时效的密码添加的时间记录

    lock_Tmp_pwdID = "" # 添加临时密码是返回的pwdID，不可删除
    lock_Tmp_AddTime=""# 添加临时密码时的时间记录

    lockPwd_editPwd_zuKe=configfile.getLockInfo()["lockPwd_editPwd_zuKe"] #修改后的租客密码
    lockPwd_editPwd_gj=configfile.getLockInfo()["lockPwd_editPwd_gj"] #修改后的管家密码
    lockPwd_editPwd_gj_pwdID=0 #对应上个管家密码的编号，因为后面去检查权限动态的时候，要用到

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
    def test_deviceCtrl_lockPwd_addPwd_zuKe_StatusCode(self):
        '''
        根据范爷跟张建反馈，后续31,51,06,04Pro都只有一个管家密码
        之前5个管家密码，主要是由warm家那边提出来的，5个管家密码的锁有：03,04,05这3把锁
        因此，这里添加管家密码，就不做测试
        :return:
        '''
        r = requests.post(self.apiHostPrefix + self.deviceCtrllockPwd + 'addPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s' % (
            self.lockDeviceID,self.lockNewAddZuKePwd,"3", self.mtoken))
        rsp = json.loads(r.text)
        log.Log("addPwd_zuKe_StatusCode下发新增租客密码指令成功！！！租客密码为%s"%self.lockNewAddZuKePwd)

        getLockApi.lockNewAddZuKePwd_pwdID=rsp["result"]["pwdID"]
        self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')
    def test_deviceCtrl_lockPwd_addPwd_zuKe_CheckStatusAccess(self):
        # 拿到返回来的pwdID,跟从数据库里面拿到的做对比
        # 由于pwdID都是由云端生成的，这里转换一下，换别名，看看门锁上有没有这个密码的别名
        # 通过id找到别名，然后通过数据的别名跟中控同步上来的别名做对比
        # findResult=0 #如果在数据库中找到权限动态，则将findResult 设置为1
        # checkAccessList=[]
        pwdIDSql="SELECT pwdAlias from device_pwd_info WHERE id="+"\'"+str(getLockApi.lockNewAddZuKePwd_pwdID)+"\'"
        db_pwdAlias=self.db.dbOperation(pwdIDSql)
        db_pwdAlias=db_pwdAlias[0][0]
        getLockApi.lockNewAddZuKePwd_Alias=db_pwdAlias
        #从中控获取密码别名
        # self.lockTool.lockSyncPwd(self.lockDeviceID,self.username,self.password) #  这个主要是做密码通过的。根据门锁的设备ID做密码同步工作
        #根据501反馈，从云端做数据同步，立马发，立马回，但是，为了保险起见这里还是休眠3秒钟
        # 目前该接口的密码管理，还是有云端管理的，需要等权限动态返回来。那么就循环5次，做权限动态验证。
        # 由于密码权限动态上报的时间不确定，所以在检查的时候，先休眠一分钟
        # time.sleep(60)
        findResult=self.lockTool.checkStatusAccessInDB(self.lockDeviceID,self.reportTime,self.allPwdAddTime,db_pwdAlias,3)
        log.Log("addPwd_zuKe_CheckStatusAccess新增租客密码权限动态已经校验完成！！！")
        # for looptime in range(2):
        #     getCCpwdAliasSql="SELECT report_content FROM log_report WHERE device_id="+"\'"+self.lockDeviceID+"\'"+"and url_path='status/access' AND report_content LIKE '%\"type\":3%' ORDER BY report_time DESC "
        #     getCenterControlPwdAlias=self.db.dbOperation(getCCpwdAliasSql,db='danbay_task')
        #     # 遍历结果，看看能否找到权限动态
        #     for singleAccess in range(len(getCenterControlPwdAlias)):
        #         accessRecord=getCenterControlPwdAlias[singleAccess][0]
        #         accessRecord=accessRecord.split("payLoadString=")[1] # 对应为：{"type":3,"action":1,"op_code":0,"alias":"Preset2","time":"180427103610"}
        #         accessRecord=json.loads(accessRecord) #将上面的转为json数据
        #         accessRecordTime=accessRecord["time"]
        #         checkAccessList.append(accessRecord)
        #         if accessRecordTime>getLockApi.zuKePwdAddTime:# 如果从数据库中获取到的时间比门锁添加的时间大，那么，就将该该条记录加入到列表中，供后续比对，过滤完之后，就停止过滤
        #             if db_pwdAlias in accessRecord["alias"]:
        #                 findResult=1
        #                 break
        #     time.sleep(60*3)
        self.assertEquals(1, findResult[0], msg=u'新增租客密码后，没有收到权限动态上报，就发送密码出来了。调用API新增密码时间%s，检查权限动态列表为：%s'%(getLockApi.zuKePwdAddTime,findResult[1]))
    def test_deviceCtrl_lockPwd_addPwdWithDate_zuKe_StatusCode(self):
        # 新增密码前，记录一下时间，供后面去log report 找日志使用
        d1=datetime.datetime.now()
        d3=d1.strftime("%Y-%m-%d %H:%M:%S")
        # getLockApi.addPwdWithDate_AddTime=d1
        # getLockApi.addPwdWithDate_AddTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        # getLockApi.addPwdWithDate_AddTime = getLockApi.addPwdWithDate_AddTime[2:]
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'addPwdWithDate?deviceId=%s&password=%s&pwdType=%s&mtoken=%s&beginTime=%s&endTime=%s' % (
                self.lockDeviceID, self.lockPwd_addPwdWithDate, "3", self.mtoken,d3,d1 + datetime.timedelta(hours=3)))
        rsp = json.loads(r.text)
        getLockApi.addPwdWithDate_pwdID = rsp["result"]["pwdID"]
        self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')
    def test_deviceCtrl_lockPwd_addPwdWithDate_zuKe_CheckStatusAccess(self):
        pwdIDSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(getLockApi.addPwdWithDate_pwdID) + "\'"
        db_pwdAlias = self.db.dbOperation(pwdIDSql)
        db_pwdAlias = db_pwdAlias[0][0]
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,db_pwdAlias, 3)
        # for looptime in range(2):
        #     log.Log("开始第%s 次循环"%(looptime+1))
        #     getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + self.lockDeviceID + "\'" + \
        #                        "AND url_path='status/access' AND report_content LIKE '%\"type\":3%' AND report_time LIKE '" + sqlDay + "%'ORDER BY report_time DESC "
        #     getCenterControlPwdAlias = self.db.dbOperation(getCCpwdAliasSql, db='danbay_task')
        #     # 遍历结果，看看能否找到权限动态
        #     for singleAccess in range(len(getCenterControlPwdAlias)):
        #         accessRecord = getCenterControlPwdAlias[singleAccess][0]
        #         accessRecord = accessRecord.split("payLoadString=")[
        #             1]  # 对应为：{"type":3,"action":1,"op_code":0,"alias":"Preset2","time":"180427103610"}
        #         accessRecord = json.loads(accessRecord)  # 将上面的转为json数据
        #         accessRecordTime = accessRecord["time"]
        #         checkAccessList.append(accessRecord)
        #         if accessRecordTime > getLockApi.zuKePwdAddTime:  # 如果从数据库中获取到的时间比门锁添加的时间大，那么，就将该该条记录加入到列表中，供后续比对，过滤完之后，就停止过滤
        #             if db_pwdAlias in accessRecord["alias"]:
        #                 findResult = 1
        #                 log.Log("从数据库中找到了添加的密码别名，记录为：%s"%accessRecord)
        #                 break
        #     log.Log("开始休眠3分钟")
        #     time.sleep(60 * 3)
        self.assertEquals(1, findResult[0], msg=u'新增租客密码后，没有收到权限动态上报，就发送密码出来了。调用API新增密码时间%s，检查权限动态列表为：%s' % (
            getLockApi.zuKePwdAddTimeWithDate, findResult[1]))
    def test_deviceCtrl_lockPwd_addPwd_tmp_StatusCode(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'addPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s' % (
                self.lockDeviceID, self.lockPwd_addPwd_Tmp, "0", self.mtoken))
        rsp = json.loads(r.text)
        getLockApi.lock_Tmp_pwdID = rsp["result"]["pwdID"]
        log.Log("添加临时密码：%s，密码编号pwdID为：%s"%(self.lockPwd_addPwd_Tmp,getLockApi.lock_Tmp_pwdID))
        self.assertEquals(200, r.status_code, msg=u'添加临时密码API返回的状态码不等于200')
    def test_deviceCtrl_lockPwd_addPwd_tmp_CheckStatusAccess(self):
        pwdIDSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(
            getLockApi.lock_Tmp_pwdID) + "\'"
        db_pwdAlias = self.db.dbOperation(pwdIDSql)
        db_pwdAlias = db_pwdAlias[0][0]
        findResult=self.lockTool.checkStatusAccessInDB(self.lockDeviceID,self.reportTime, self.allPwdAddTime,db_pwdAlias,0)
        #这里用try 只是为了跳出多重循环！！！

        # try:
        #     for looptime in range(2):
        #         log.Log("开始第%s 次循环去找权限动态" % (looptime + 1))
        #         getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + self.lockDeviceID + "\'" + \
        #                            "AND url_path='status/access' AND report_content LIKE '%\"type\":0%' AND report_time LIKE '" + sqlDay + "%'ORDER BY report_time DESC "
        #         getCenterControlPwdAlias = self.db.dbOperation(getCCpwdAliasSql, db='danbay_task')
        #         # 遍历结果，看看能否找到权限动态
        #         for singleAccess in range(len(getCenterControlPwdAlias)):
        #             dbaccessRecord = getCenterControlPwdAlias[singleAccess][0]
        #             accessRecord = dbaccessRecord.split("payLoadString=")[
        #                 1]  # 对应为：{"type":3,"action":1,"op_code":0,"alias":"Preset2","time":"180427103610"}
        #             accessRecord = json.loads(accessRecord)  # 将上面的转为json数据
        #             accessRecordTime = accessRecord["time"]
        #             checkAccessList.append(accessRecord)
        #             if accessRecordTime > getLockApi.zuKePwdAddTime:  # 如果从数据库中获取到的时间比门锁添加的时间大，那么，就将该该条记录加入到列表中，供后续比对，过滤完之后，就停止过滤
        #                 if db_pwdAlias in accessRecord["alias"]:
        #                     findResult =1
        #                     log.Log("从数据库中找到了添加的密码别名，记录为：%s" % dbaccessRecord)
        #                     raise Exception
        #         log.Log("log report 中没有找到数据库权限动态，开始休眠3分钟")
        #         time.sleep(60 * 3)
        # except Exception:
        #     pass
        self.assertEquals(1, findResult[0], msg=u'新增临时密码后，没有收到权限动态上报，就发送密码出来了。调用API新增临时密码时间%s，检查权限动态列表为：%s' % (
            getLockApi.lock_Tmp_AddTime, findResult[1]))
    def test_deviceCtrl_lockPwd_editPwd_zuKe_StatusCode(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'editPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s&pwdID=%s' % (
                self.lockDeviceID, self.lockPwd_editPwd_zuKe, "3", self.mtoken,getLockApi.lockNewAddZuKePwd_pwdID))
        log.Log("修改租客密码指令发送成功，新修改后的租客密码是：%s"%self.lockPwd_editPwd_zuKe)
        self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')
    def test_deviceCtrl_lockPwd_editPwd_zuKe_CheckStatusAccess(self):
        pwdIDSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(getLockApi.lockNewAddZuKePwd_pwdID) + "\'"
        db_pwdAlias = self.db.dbOperation(pwdIDSql)
        db_pwdAlias = db_pwdAlias[0][0]

        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,db_pwdAlias, 4)
        log.Log("完成修改租客密码的动态权限检查。需要修改的密码的密码别名是：%s" % db_pwdAlias)
        self.assertEquals(1, findResult[0], msg=u'新增临时密码后，没有收到权限动态上报，就发送密码出来了。调用API新增临时密码时间%s，检查权限动态列表为：%s' % (
            getLockApi.lock_Tmp_AddTime, findResult[1]))
    def test_deviceCtrl_lockPwd_editPwd_gj_StatusCode(self):
        gj_pwdIDSql = "SELECT id from device_pwd_info WHERE deviceInfo=(SELECT id FROM device_info WHERE deviceId=" + "\'" + self.lockDeviceID + "\'" + ") AND pwdType='2';"
        gj_pwdIDResult = self.db.dbOperation(gj_pwdIDSql)
        if gj_pwdIDResult:
            gj_pwdID = gj_pwdIDResult[0][0]
            getLockApi.lockPwd_editPwd_gj_pwdID = gj_pwdID
            log.Log("被选中修改密码的管家ID是：%s" % gj_pwdID)

            r = requests.post(
                self.apiHostPrefix + self.deviceCtrllockPwd + 'editPwd?deviceId=%s&password=%s&pwdType=%s&pwdID=%s&=mtoken%s' % (
                    self.lockDeviceID, self.lockPwd_editPwd_gj, "2", gj_pwdID, self.mtoken))
            log.Log("修改管家密码指令发送成功，新修改后的管家密码是：%s" % self.lockPwd_editPwd_gj)
            self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')
        else:
            no_gjPwd = 1
            self.assertEquals(0, no_gjPwd, msg=u"该门锁没有管家密码，无法测试修改管家密码的功能！！！！！！")
    def test_deviceCtrl_lockPwd_editPwd_gj_CheckStatusAccess(self):
        if getLockApi.lockPwd_editPwd_gj_pwdID:

            pwdIDSql = "SELECT pwdAlias from device_pwd_info WHERE id=" + "\'" + str(
            getLockApi.lockPwd_editPwd_gj_pwdID) + "\'"
            db_pwdAlias = self.db.dbOperation(pwdIDSql)
            db_pwdAlias = db_pwdAlias[0][0]
            getLockApi.lock_gj_alias=db_pwdAlias
            findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                             db_pwdAlias, 5)
            log.Log("完成修改管家密码的动态权限检查。需要修改的密码的密码别名是：%s" % db_pwdAlias)
            self.assertEquals(1, findResult[0], msg=u'新增临时密码后，没有收到权限动态上报，就发送密码出来了。调用API新增临时密码时间%s，检查权限动态列表为：%s' % (
                getLockApi.lock_Tmp_AddTime, findResult[1]))
        else:
            self.assertEquals(0, 1, msg=u"该门锁没有管家密码，不能去检查动态权限！！！！！！")
    def test_deviceCtrl_lockPwd_updatePwd_freeze_zuKe(self):
        # 这里先假设前面的密码都已经成功加进去了。异常情况，后面再处理。针对异常情况，后面可以通过全局性的标志来决定改用例是否能被执行
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "0","3", getLockApi.lockNewAddZuKePwd_pwdID, self.mtoken))
        log.Log("冻结租客密码指令发送成功，冻结的租客pwdID是：%s" % getLockApi.lockNewAddZuKePwd_pwdID)
        updatePwd_stop_zuKe_time=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'冻结租客密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockNewAddZuKePwd_Alias, "updatePwd_freeze_zuke")
        log.Log("查找的权限动态列表：%s"%findResult[1])
        self.assertEquals(1, findResult[0], msg=u'冻结租客密码后，没有收到权限动态上报。调用API冻结密码时间%s，检查权限动态列表为：%s' % (
            updatePwd_stop_zuKe_time, findResult[1]))
    def test_deviceCtrl_lockPwd_updatePwd_unfreeze_zuKe(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "1", "3", getLockApi.lockNewAddZuKePwd_pwdID, self.mtoken))
        log.Log("解冻租客密码指令发送成功，解冻的租客pwdID是：%s" % getLockApi.lockNewAddZuKePwd_pwdID)
        updatePwd_unstop_zuKe_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'冻结租客密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockNewAddZuKePwd_Alias, "updatePwd_unfreeze_zuke")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'解冻租客密码后，没有收到权限动态上报。调用API解冻密码时间%s，检查权限动态列表为：%s' % (
            updatePwd_unstop_zuKe_time, findResult[1]))

    def test_deviceCtrl_lockPwd_updatePwd_freeze_gj(self):
        # 这里先假设前面的密码都已经成功加进去了。异常情况，后面再处理。针对异常情况，后面可以通过全局性的标志来决定改用例是否能被执行
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "0", "2", getLockApi.lockPwd_editPwd_gj_pwdID, self.mtoken))
        log.Log("冻结管家密码指令发送成功，冻结的管家pwdID是：%s" % getLockApi.lockPwd_editPwd_gj_pwdID)
        updatePwd_stop_gj_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'冻结管家密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lock_gj_alias, "updatePwd_freeze_gj")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'冻结管家密码后，没有收到权限动态上报。调用API冻结密码时间%s，检查权限动态列表为：%s' % (
            updatePwd_stop_gj_time, findResult[1]))
    def test_deviceCtrl_lockPwd_updatePwd_unfreeze_gj(self):
        # 这里先假设前面的密码都已经成功加进去了。异常情况，后面再处理。针对异常情况，后面可以通过全局性的标志来决定改用例是否能被执行
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "1", "2", getLockApi.lockPwd_editPwd_gj_pwdID, self.mtoken))
        log.Log("解冻管家密码指令发送成功，解冻的管家pwdID是：%s" % getLockApi.lockPwd_editPwd_gj_pwdID)
        updatePwd_unstop_gj_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'解冻管家密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lock_gj_alias, "updatePwd_unfreeze_gj")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'解冻管家密码后，没有收到权限动态上报。调用API解冻管家密码时间%s，检查权限动态列表为：%s' % (
            updatePwd_unstop_gj_time, findResult[1]))


    def test_deviceCtrl_lockPwd_delPwd_zuKe(self):
        # --getLockApi.lockNewAddZuKePwd_pwdID
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'delPwd?deviceId=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "3",getLockApi.lockNewAddZuKePwd_pwdID , self.mtoken))
        log.Log("删除租客密码指令发送成功，删除的租客pwdID是：%s" % getLockApi.lockNewAddZuKePwd_pwdID)
        updatePwd_stop_zuKe_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'删除租客密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockNewAddZuKePwd_Alias, "delPwd_zuke")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'删除租客密码后，没有收到权限动态上报。调用API冻结密码时间%s，' % (
            updatePwd_stop_zuKe_time))
    def test_deviceCtrl_lockPwd_delPwd_tmp(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'delPwd?deviceId=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
                self.lockDeviceID, "0", getLockApi.lock_Tmp_pwdID, self.mtoken))
        log.Log("删除临时密码指令发送成功，删除的临时密码的pwdID是：%s，API返回的状态码是：%s" % (getLockApi.lock_Tmp_pwdID,r.status_code))
        updatePwd_stop_zuKe_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.assertEquals(200, r.status_code, msg=u'删除临时密码API返回的状态码不等于200')
        findResult = self.lockTool.checkStatusAccessInDB(self.lockDeviceID, self.reportTime, self.allPwdAddTime,
                                                         getLockApi.lockNewAddZuKePwd_Alias, "delPwd_tmp")
        log.Log("查找的权限动态列表：%s" % findResult[1])
        self.assertEquals(1, findResult[0], msg=u'删除租客密码后，没有收到权限动态上报。调用API冻结密码时间%s，' % (
            updatePwd_stop_zuKe_time))





# a=getLockApi()
# a.test_getLockList()
# a=getLockList()
# a.test_getDeviceListAllWithCorrectInfo()