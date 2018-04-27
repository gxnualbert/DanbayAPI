#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:albert.chen
@file: dboperation.py
@time: 2018/04/25/22:11
"""
import MySQLdb

class dbOperate():
    def dbOperation(self,sql,db='danbay_device'):
        conn = MySQLdb.connect(
            host='120.77.236.177',
            port=3307,
            user='root',
            passwd='LoveDanbayWrite!',
            db=db,
            charset="utf8"
        )
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return results


# a=dbOperate()
# lockOnlineStatusSql="SELECT online FROM device_info WHERE deviceId='b8e09c3e18dba4ea934152a3026945e0'"
# aaa=a.dbOperation(lockOnlineStatusSql)
# print aaa[0][0]