#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: readconf.py
@time: 2017/12/26/11:58
"""
import ConfigParser
import os

class ReadConfigFile():

    # confPath = os.path.abspath(os.path.dirname(os.getcwd())) + "\\api_test\\conf.cfg"
    # confPath=os.path.dirname(os.getcwd())+"\\conf.cfg"
    confPath=os.getcwd()+"\\conf.cfg"
    cf = ConfigParser.ConfigParser()
    cf.read(confPath)

    def getBasicConf(self):
        host=self.cf.get("BasicConf", "host")
        username=self.cf.get("BasicConf", "username")
        password=self.cf.get("BasicConf", "password")
        apiHostPrefix="http://"+host+"/system/"
        confinfo={}
        confinfo["host"]=host
        confinfo["username"]=username
        confinfo["password"]=password
        confinfo["apiHostPrefix"]=apiHostPrefix

        return confinfo

    def getLockInfo(self):
        lockInfo={}
        lockInfo["lockDeviceID"]=self.cf.get("LockInfo", "lockDeviceID")
        lockInfo["lockPwd_addPwd_zuke"]=self.cf.get("LockInfo", "lockPwd_addPwd_zuke")
        lockInfo["lockPwd_addPwd_gj"] = self.cf.get("LockInfo", "lockPwd_addPwd_gj")
        lockInfo["lockPwd_addPwd_tmp"] = self.cf.get("LockInfo", "lockPwd_addPwd_tmp")
        lockInfo["lockPwd_addPwdWithDate_zuke"]=self.cf.get("LockInfo", "lockPwd_addPwdWithDate_zuke")
        lockInfo["lockPwd_editPwd_zuke"]=self.cf.get("LockInfo", "lockPwd_editPwd_zuke")
        lockInfo["lockPwd_editPwd_gj"]=self.cf.get("LockInfo", "lockPwd_editPwd_gj")
        return  lockInfo

# a=ReadConfigFile()
# print a.getBasicConf()["password"]