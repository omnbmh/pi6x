#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

'''
    本程序主要用于批量修复用户的收益
    仅修复执行执行状态为成功的计划执行的收益 计划执行状态不对的请先修复计划执行的状态
'''

import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('zqb')
logger.info('日志模块加载成功')

import json
import datetime
import math
import zqblib
import time
jrt = zqblib.login('chendezhi','888888')
    
def batch():
    '''
    读取planid.txt文件 获得计划id 批量执行
    '''
    logger.info('执行任务开始')
    for line in open("planid.txt"):
        planid = line.strip('\r\n')
        zqb = zqblib.ZQB(planid)
        planexecutions = zqb.select_plan_execution(0)
        if zqb.plan and planexecutions:
            for i in range(0,len(planexecutions)):
                cur_pe = planexecutions[i]
                next_pe = None if i == 0 else planexecutions[i-1]
                
                loanmoney = zqb.select_loanmoney()
                if not loanmoney:
                    loanmoney = zqb.insert_loanmoney(zqb.plan)
                loanmoneydets = zqb.select_loanmoneydet(cur_pe)
                if not loanmoneydets:
                    loanmoneydets = zqb.insert_loanmoneydet(cur_pe,loanmoney)
                
                zqb.update_dayinterestlog(cur_pe,next_pe,len(planexecutions) - i)
        zqb.update_plannl()
        time.sleep(float(5))        
        
    logger.info('执行任务结束')
    
batch()
