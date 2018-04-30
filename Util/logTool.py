#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:albert.chen
@file: logTool.py
@time: 2018/04/27/22:19
"""


import logging
import logging.handlers
import time,os


import logging

# 参考文章https://www.cnblogs.com/dkblog/archive/2011/08/26/2155018.html
class AddLog(object):
    def __init__(self):
        pass
    @classmethod
    def Log(self,logmessage,loglevel="info"):
        cwd = os.getcwd()
        # logFolder=os.path.dirname(cwd)+ "\\API_Test_Report\\"+ "log_"+time.strftime("%Y-%m-%d")
        logFolder=cwd+ "\\API_Test_Report\\"+ "log_"+time.strftime("%Y-%m-%d")
        if not os.path.exists(logFolder):
            os.mkdir(logFolder)
        LOG_FILE =  logFolder +"\\"+ time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time())) + ".log"
        # Logger=time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))
        # handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
        # fmt = '%(asctime)s - %(filename)s:- %(message)s'
        # # fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        #
        # formatter = logging.Formatter(fmt)  # 实例化formatter
        # handler.setFormatter(formatter)  # 为handler添加formatter
        #
        # logger = logging.getLogger(Logger)  # 获取名为tst的logger
        # logger.addHandler(handler)  # 为logger添加handler
        # logger.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=LOG_FILE,
                            filemode='w')
        #################################################################################################
        # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        #################################################################################################
        if loglevel=="debug":
            logging.debug(logmessage.decode("utf-8"))
        elif loglevel=="info":
            logging.info(logmessage.decode("utf-8"))
        elif loglevel=="warning":
            logging.warning(logmessage.decode("utf-8"))


# a=AddLog()
# a.Log("dddddddddddd")