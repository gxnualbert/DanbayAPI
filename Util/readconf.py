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
        lockInfo["lockNewAddZuKePwd"]=self.cf.get("LockInfo", "lockNewAddZuKePwd")
        lockInfo["lockPwd_editPwd_zuKe"]=self.cf.get("LockInfo", "lockPwd_editPwd_zuKe")
        lockInfo["lockPwd_addPwd_Tmp"]=self.cf.get("LockInfo", "lockPwd_addPwd_Tmp")
        lockInfo["lockPwd_addPwdWithDate"]=self.cf.get("LockInfo", "lockPwd_addPwdWithDate")
        lockInfo["lockPwd_editPwd_gj"]=self.cf.get("LockInfo", "lockPwd_editPwd_gj")

        return  lockInfo

# a=ReadConfigFile()
# print a.getBasicConf()["password"]