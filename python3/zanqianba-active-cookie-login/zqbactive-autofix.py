#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

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
    for line in open("planid.txt"):
        line = line.strip('\r\n')
        zqb = zqblib.ZQB(line)
        if (not zqb.plan) and (not zqb.planexecutions):
            continue
        
        planexecution = zqb.planexecutions[0] # 取最新的计划执行
        loanmoney = zqb.select_loanmoney()
        if not loanmoney:
            loanmoney = zqb.insert_loanmoney(zqb.plan)
        loanmoneydets = zqb.select_loanmoneydet(planexecution)
        if not loanmoneydets:
            loanmoneydets = zqb.insert_loanmoneydet(planexecution,loanmoney)
        
batch()
