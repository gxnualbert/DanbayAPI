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
from Util.readconf import ReadConfigFile
from Util.getToken import token
from Util.dboperation import dbOperate
from Util.lockUtil import lockCommonUtil
import time
# class test_getDeviceListAll(unittest.TestCase):

class getLockApi(unittest.TestCase):

    configfile = ReadConfigFile()
    apiHostPrefix = configfile.getBasicConf()["apiHostPrefix"]
    username=configfile.getBasicConf()["username"]
    password=configfile.getBasicConf()["password"]

    lockDeviceID=configfile.getLockInfo()["lockDeviceID"]
    lockNewAddZuKePwd=configfile.getLockInfo()["lockNewAddZuKePwd"]
    lockNewAddZuKePwd_pwdID=""

    lockTool=lockCommonUtil()

    tk = token()
    mtoken = tk.getToken()
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
    def test__getLockInfo_Message(self):
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

        getLockApi.lockNewAddZuKePwd_pwdID=rsp["result"]["pwdID"]

        self.assertEquals(200, r.status_code, msg=u'添加租客密码API返回的状态码不等于200')

    def test_deviceCtrl_lockPwd_addPwd_zuKe_CheckpwdID(self):
        # 拿到返回来的pwdID,跟从数据库里面拿到的做对比
        # 由于pwdID都是由云端生成的，这里转换一下，换别名，看看门锁上有没有这个密码的别名
        # 通过id找到别名，然后通过数据的别名跟中控同步上来的别名做对比
        pwdIDSql="SELECT pwdAlias from device_pwd_info WHERE id="+"\'"+str(getLockApi.lockNewAddZuKePwd_pwdID)+"\'"

        db_pwdAlias=self.db.dbOperation(pwdIDSql)
        db_pwdAlias=db_pwdAlias[0][0]

        #从中控获取密码别名

        self.lockTool.lockSyncPwd(self.lockDeviceID,self.username,self.password)
        #根据501反馈，从云端做数据同步，立马发，立马回，但是，为了保险起见这里还是休眠3秒钟
        time.sleep(3)

        getCCpwdAliasSql="SELECT err_msg FROM log_report WHERE device_id="+"\'"+self.lockDeviceID+"\'"+" and url_path= 'ctrl/pwd_info' ORDER BY report_time DESC"

        getCenterControlPwdAlias=self.db.dbOperation(getCCpwdAliasSql,db='danbay_task')

        getCenterControlPwdAlias=getCenterControlPwdAlias[0][0]
        getCenterControlPwdAliaspayload=getCenterControlPwdAlias.split("payload")[1]

        self.assertIn(db_pwdAlias, getCenterControlPwdAliaspayload,msg=u"数据库中的密码别名：%s不存在于中控同步上来的密码别名中：%s"%(db_pwdAlias,getCenterControlPwdAliaspayload))
        # 判断数据库中密码别名是否在中控里面






    def test_deviceCtrl_lockPwd_addPwd_tmp_StatusCode(self):
        r = requests.post(
            self.apiHostPrefix + self.deviceCtrllockPwd + 'addPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s' % (
                self.lockDeviceID, self.lockNewAddZuKePwd, "0", self.mtoken))
        rsp = json.loads(r.text)

        self.lockNewAddZuKePwd_pwdID = rsp["result"]["pwdID"]
        self.assertEquals(200, r.status_code, msg=u'添加临时密码API返回的状态码不等于200')










    def test_getLockPwdList_Status(self):

        r = requests.post(self.apiHostPrefix +self.deviceInfo +'getLockPwdList?deviceId=%s&mtoken=%s' % (
        "b8e09c3e18dba4ea934152a3026945e0", self.mtoken))
        self.assertEquals(200, r.status_code)
    def test_getLockPwdList_(self):
        pass
    def test_lockPwd_addPwd_tmp(self):

        # 要从配置文件中读取锁 的deviceid
        #需要所，暂时不做
        r = requests.post(self.apiHostPrefix + 'getLockInfo?deviceId=%s&mtoken=%s' % (
            "8f1d4c722da04f9237e20f97ac5f5188", self.mtoken))
        self.assertEquals(200, r.status_code)
    def test_lockPwd_addPwd_gj(self):

        # 要从配置文件中读取锁 的deviceid
        #需要所，暂时不做
        r = requests.post(self.apiHostPrefix + 'getLockInfo?deviceId=%s&mtoken=%s' % (
            "8f1d4c722da04f9237e20f97ac5f5188", self.mtoken))
        self.assertEquals(200, r.status_code)

    def test_lockPwd_addPwd_zuke(self):

        # 要从配置文件中读取锁 的deviceid
        #需要所，暂时不做
        r = requests.post(self.apiHostPrefix + 'getLockInfo?deviceId=%s&mtoken=%s' % (
            "8f1d4c722da04f9237e20f97ac5f5188", self.mtoken))
        self.assertEquals(200, r.status_code)

    def test_lockPwd_addPwdWithDate_temp(self):
        r = requests.post(self.apiHostPrefix + 'getLockInfo?deviceId=%s&mtoken=%s' % (
            "8f1d4c722da04f9237e20f97ac5f5188", self.mtoken))
        self.assertEquals(200, r.status_code)
    def test_lockPwd_addPwdWithDate_gj(self):
        r = requests.post(self.apiHostPrefix + 'getLockInfo?deviceId=%s&mtoken=%s' % (
            "8f1d4c722da04f9237e20f97ac5f5188", self.mtoken))
        self.assertEquals(200, r.status_code)

    def test_lockPwd_addPwdWithDate_zuke(self):
        r = requests.post(self.apiHostPrefix + 'getLockInfo?deviceId=%s&mtoken=%s' % (
            "8f1d4c722da04f9237e20f97ac5f5188", self.mtoken))
        self.assertEquals(200, r.status_code)


    def test_lockPwd_editPwd_gj(self):
        pass

    def test_lockPwd_editPwd_zuke(self):
        pass
    def test_lockPwd_editPwdWithDate_gj(self):
        pass

    def test_lockPwd_editPwdWithDate_zuke(self):
        pass

    def test_lockPwd_delPwd_gj(self):
        pass

    def test_lockPwd_delPwd_tmp(self):
        pass
    def test_lockPwd_delPwd_zuke(self):
        pass

    def test_lockPwd_updatePwd_gj(self):
        pass

    def test_lockPwd_updatePwd_zuke(self):
        pass



# a=getLockApi()
# a.test_getLockList()
# a=getLockList()
# a.test_getDeviceListAllWithCorrectInfo()