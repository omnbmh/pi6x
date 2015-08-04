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
    #for line in open("planexecutionid.txt"):
        line = line.strip('\r\n')
        zqb = zqblib.ZQB(line)
        if (not zqb.plan):
            continue
        
        #计划的开始日期
        start_date = zqb.plan['createtime']
        #计划的截止日期
        end_date = zqb.plan['enddate']
        #当前期数
        now_period = zqb.plan['nowperiod']
        
        one_month = datetime.timedelta(months=1)
        
        now_p = 2;
        while start_date + one_month > datetime.now():
            start_date += one_month
            now_p+=1
            
        #now_p -= 1
        #start_date -= one_month
        
        if start_date < end_date:
            zqb.insert_planexecution()
        
batch()
