#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

'''
    本脚本主要将计划执行状态为投资处理中的修改为成功
'''

# config logging
import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('zqb')
logger.info('日志模块加载成功')

import json
import datetime
import math
import zqblib
jrt = zqblib.login('chendezhi','888888')
    
def batch():
    '''
    读取planid.txt文件 获得计划id 批量执行
    '''
    #for line in open("planid.txt"):
    for line in open("planexecutionid.txt"):
        line = line.strip('\r\n')
        zqb = zqblib.ZQB()
        planexecution = zqb.select_plan_execution_by_id(line,11)
        if planexecution:
            zqb.update_planexecution(planexecution,'0')
        
batch()
