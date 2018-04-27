#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author:albert.chen
@file: CheckReportDir.py
@time: 2017/12/11/17:42
"""
import os,time

class CheckReportPath():


    @staticmethod
    def getReportPath():
        cwd = os.getcwd()
        # parentpath = os.path.abspath(os.path.join(s, ".."))
        folderpath = cwd + "\\API_Test_Report\\\\" + time.strftime("%Y-%m-%d")

        if os.path.exists(folderpath):
            return folderpath
        else:
            os.makedirs(folderpath)
            return folderpath
