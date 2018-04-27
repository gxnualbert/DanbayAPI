#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:albert.chen
@file: test_suite.py
@time: 2017/12/01/10:00
"""
import requests
import json
import unittest
import time
import HTMLTestRunner

class DBAPITest():
    # host='http://test.www.danbay.cn/system'
    host='http://www.danbay.cn/system'
    # host='http://192.168.16.100:8689/system'


    def test_getToken(self,mc_username,mc_password,ticket_consume_url,return_url,random_code):
        payload = {'mc_username': mc_username, 'mc_password': mc_password, 'ticket_consume_url': ticket_consume_url,
                   'return_url': return_url, 'random_code': random_code}
        r = requests.post(self.host+'/connect', data=payload)
        mtoekn = r.url.split('mtoken=')[1]
        print mtoekn
        print r.status_code
        return mtoekn
    def test_getAccess(self,mc_username,mc_password,random_code):
        payload = {'mc_username': mc_username, 'mc_password': mc_password,
                    'random_code': random_code}
        r = requests.post(self.host + '/loginAccess',data=payload )
        rsp= r.text
        rsp1=json.loads(rsp,encoding='utf-8')
        # print rsp1['result']['mtoken']
        return rsp1['result']['mtoken']

    def test_getDeviceListAll(self,mtoken):
        r = requests.post(self.host+'/deviceInfo/getDeviceIistAll?mtoken=%s'%mtoken)
        print r.text
    def test_getLockList(self,mtoken):
        r = requests.post(self.host + '/deviceInfo/getLockIist?mtoken=%s' % mtoken)
        print r.text

    def test_getLockInfo(self,deviceId,mtoken):
        r = requests.post(self.host + '/deviceInfo/getLockInfo?deviceId=%s&mtoken=%s' % (deviceId, mtoken))
        print r.text
    def test_getLockPwdList(self,deviceId,mtoken):
        r = requests.post(self.host + '/deviceInfo/getLockPwdList?deviceId=%s&mtoken=%s' % (deviceId,mtoken))
        print r.text
    def test_lockPwd_addPwd(self,deviceId,password,pwdType,mtoken):
        r = requests.post(self.host + '/deviceCtrl/lockPwd/addPwd?deviceId=%s&password=%s&pwdType=%s&mtoken=%s' % (
            deviceId, password, pwdType, mtoken))
        print r.text
    def test_lockPwd_editPwd(self,deviceId,pwdType,password,pwdID,mtoken):
        r = requests.post(self.host + '/deviceCtrl/lockPwd/editPwd?deviceId=%s&pwdType=%s&password=%s&pwdID=%s&mtoken=%s' % (
        deviceId, pwdType,password,pwdID, mtoken))
        print r.text
    def test_lockPwd_delPwd(self,deviceId,pwdType,pwdID,mtoken):
        r = requests.post(self.host + '/deviceCtrl/lockPwd/delPwd?deviceId=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
            deviceId, pwdType, pwdID, mtoken))
        print r.text
    def test_lockPwd_updatePwd(self,deviceId,updateType,pwdType,pwdID,mtoken):
        r = requests.post(self.host + '/deviceCtrl/lockPwd/updatePwd?deviceId=%s&updateType=%s&pwdType=%s&pwdID=%s&mtoken=%s' % (
            deviceId,updateType, pwdType, pwdID, mtoken))
        print r.text
    # def test_getEnergyDeviceList(self,mtoken):
    def getEnergyDeviceList(self,mtoken):
        r = requests.post(self.host + '/deviceInfo/getEnergyDeviceList?mtoken=%s' % mtoken)
        print r.text
    def test_getEnergyDeviceInfo(self,deviceId,mtoken):
        r=requests.post(self.host+'/deviceInfo/getEnergyDeviceInfo?deviceId=%s&mtoken=%s'%(deviceId,mtoken))
        print r.text
    def test_getEnergyDailyReading(self,deviceId,readTime,mtoken):
        r = requests.post(self.host + '/deviceInfo/getEnergyDailyReading?deviceId=%s&readTime=%s&mtoken=%s' % (deviceId,readTime, mtoken))
        print r.text
    def syncHouse(self,apartmentType,apartmentList,mtoken):
        payload={'apartmentType':apartmentType,'apartmentList':apartmentList,'mtoken':mtoken}
        r=requests.post(self.host+'/house/sync',data=payload)
        print r.text

a=DBAPITest()
a.test_getAccess("DBShow","DBShow","123456")
token=a.test_getAccess("18555698927","55698927","123456")
# print  tt
# a.test_getToken('DBShow','DBShow','test.www.danbay.cn','www.baidu.com','123456')
# token=a.test_getToken('DBShow','DBShow','test.www.danbay.cn','www.baidu.com','123456')
# token=getAccess('18665379102','chensi123','1234')
# getAllDevice(token)
# getLockList(token)
# getLockPwdList('dfe38fba9135bfbc99203d755da41844',token)
# getLockPwdList('9999',token)
# getLockInfo('dfe38fba9135bfbc99203d755da41844',token)
# lockPwd_addPwd('dfe38fc99da41844','18369414','2',token)
# lockPwd_addPwd('dfe38fba9135bfbc99203d755da41844','18369414','2',token)
# 门锁修改密码测试没通过
# lockPwd_editPwd('dfe38fba9135bfbc99203d755da41844','3','94132566','810902',token)
# lockPwd_delPwd('dfe38fba9135bfbc99203d755da41844','2','810902',token)
# lockPwd_updatePwd('dfe38fba9135bfbc99203d755da41844','0','2','810901',token)
# getEnergyDeviceList(token)
a.getEnergyDeviceList(token)
# getEnergyDeviceInfo('dfe38fba9135bfbc99203d755da41844',token)
# getEnergyDailyReading('76f9084ceaaaeee0981b3dfb68e1d1f1','2017-11-30',token)  暂时找不到合适的设备来测这个接口


# with open('cs.txt', 'r') as f:
#    apartmenList=f.readlines()
# kk=[]
# for i in apartmenList:
#     if 'buildingId' in i:
#         t=i.split('\n')[0]
#         jsonobj=t[0:len(t) - 1]
#         jsonobj=eval(jsonobj)
#         kk.append(jsonobj)
# # apartmenList=[{"buildingId":"cs001","buildingName":"长江小区","buildingNo":"1","unit":"2","roomNo":"1","roomId":"cs1","provinceId":"440000","areaId":"440306","cityId":"440300","floor":"27"}]
# aa=json.dumps(kk)
# syncHouse('0',aa,token)

# DBAPITest=DBAPITest()
# suite = unittest.TestSuite()
#
# suite.addTest(DBAPITest.test_getToken())
#
# if __name__=="main":
#     unittest.main()








