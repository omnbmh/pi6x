#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

import json
import datetime
import math
import zqblib
jrt = zqblib.login()
    
    
SQL = "INSERT INTO ZQ_PAYLOG(PK_PAYLOG, PLANEXEXCUTIONID, CHNID, BIZID, MEDIAID, AMOUNT, STATE, RETCODE, RETINFO, CREATETIME, UPDATETIME, UPDATEUSER, DATESTATE, REMARK)VALUES('', '{7}', 'UMP', '{0}', '{2}', {5}, '0', '0000', '【支付渠道消息】交易成功', to_date('{4}', 'yyyy/mm/dd hh24:mi:ss'), to_date('{4}', 'yyyy/mm/dd hh24:mi:ss'), '06', '0', NULL);"
    
    
def batch():
    '''
    读取planid.txt文件 获得计划id 批量执行
    '''
    for line in open("buildpaylog.txt"):
        line = line.strip('\r\n')
        lineArr = line.split('    ')
        #print(SQL)
        print(SQL.format(lineArr[0],lineArr[1],lineArr[2],lineArr[3],lineArr[4],lineArr[5],lineArr[6],lineArr[7],lineArr[8]))
        
batch()
