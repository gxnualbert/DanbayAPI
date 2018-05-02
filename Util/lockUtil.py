#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:albert.chen
@file: lockUtil.py
@time: 2018/04/26/17:46
"""
import requests
from Util.logTool import AddLog as log
from Util.dboperation import dbOperate
import json
import time


class lockCommonUtil():
    db = dbOperate()
    def getCookies(self,username, password):
        loginurl = 'http://www.danbay.cn/system/goLoginning'
        payload = {'mc_username': username, 'mc_password': password, 'rememberMe': ""}
        r = requests.post(loginurl, data=payload)
        return r.cookies

    def lockSyncPwd(self,deviceID,username,password):
        reqUrl="http://test.www.danbay.cn/system/lock/socket/getPwdInfo?deviceId="+deviceID
        r = requests.post(reqUrl,  cookies=self.getCookies(username,password))

    def checkStatusAccessInDB(self,lockDeviceID,reportTime,lock_pwd_addTime,db_pwdAlias,pwdType):

        '''
        该函数主要是从log report 中检索出密码的权限动态
        :param lockDeviceID: 门锁的deviceID
        :param reportTime: 从log report 中过滤出当天的时间，精确到天
        :param lock_pwd_addTime: 密码添加的时间，主要是为了节省后面遍历查找别名记录的时间
        :param db_pwdAlias: 需要检查的密码别名
        :param pwdType:
        pwdType=4：修改租客密码
        pwdType=5：修改管家密码
        :return: findResult， 1表示找到了密码别名

        '''

        returnList=[]

        if pwdType==0:
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":0,\"action\":1,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "

        elif  pwdType==3:
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":3,\"action\":1,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType=="addPwd_gj":
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":2,\"action\":1,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "

        elif pwdType==4:
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":3,\"action\":2,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType==5:
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":2,\"action\":2,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType=="updatePwd_freeze_zuke":
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":3,\"action\":4,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType=="updatePwd_unfreeze_zuke":
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":3,\"action\":5,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType=="updatePwd_freeze_gj":
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":3,\"action\":4,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType=="updatePwd_unfreeze_gj":
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":3,\"action\":5,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType == "delPwd_zuke":
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":3,\"action\":3,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType == "delPwd_tmp":
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":0,\"action\":3,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        elif pwdType == "delPwd_gj":
            getCCpwdAliasSql = "SELECT report_content FROM log_report WHERE device_id=" + "\'" + lockDeviceID + "\'" + \
                               "AND url_path='status/access' AND report_content LIKE '%\"type\":2,\"action\":3,\"op_code\":0%' AND report_time LIKE '" + reportTime + "%'ORDER BY report_time DESC "
        try:

            for looptime in range(20):
                # log.Log("开始第%s 次循环去找权限动态" % (looptime + 1))
                getCenterControlPwdAlias = self.db.dbOperation(getCCpwdAliasSql, db='danbay_task')
                # 遍历结果，看看能否找到权限动态
                for singleAccess in range(len(getCenterControlPwdAlias)):
                    dbaccessRecord = getCenterControlPwdAlias[singleAccess][0]
                    accessRecord = dbaccessRecord.split("payLoadString=")[1]  # 对应为：{"type":3,"action":1,"op_code":0,"alias":"Preset2","time":"180427103610"}
                    accessRecord = json.loads(accessRecord)  # 将上面的转为json数据
                    accessRecordTime = accessRecord["time"]
                    if accessRecordTime > lock_pwd_addTime:  # 如果从数据库中获取到的时间比门锁添加的时间大，那么，就将该该条记录加入到列表中，供后续比对，过滤完之后，就停止过滤
                        if db_pwdAlias in accessRecord["alias"]:
                            # 是否需要检查option code=0？？有时候不是0的
                            findResult =1
                            # log.Log("从数据库中找到了添加的密码别名，记录为：%s" % dbaccessRecord)
                            returnList.append(findResult)
                            returnList.append(dbaccessRecord)

                            return returnList
                            raise Exception
                        if looptime==9 and db_pwdAlias not in accessRecord["alias"]:
                            return 0
                            raise Exception
                # log.Log("log report 中没有找到数据库权限动态，开始休眠30秒")
                time.sleep(30)
        except Exception:
            pass



