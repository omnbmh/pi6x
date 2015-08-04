#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

'''
    此脚本修复未跑批导致的当前收益未产生的问题
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
import time
jrt = zqblib.login('chendezhi','888888')
    
def batch():
    zqb = zqblib.ZQB(None)
    # 页码从1开始
    page = 1
    while (page <= 1):
        print('当前页是' + str(page))
        plans = zqb.select_all_plan(page)
        print('查询到%s条计划' % len(plans))
        for plan in plans:
            zqb.planid = plan['pkPlan']
            print(zqb.planid);
            planexecutions = zqb.select_plan_execution(0)
            if planexecutions:
                planexecution = planexecutions[0] # 取最新的计划执行
                dayintests = zqb.select_dayinterestlog(plan)
                isC = 0
                for dayintest in dayintests:
                    if dayintest['interestdate'].find('2015-07-31') >= 0:
                        print('包含7月31号的日收益')
                        isC=1
                        break
                if not isC:
                    print('不包含7月31号的日收益')
                    #插入日收益记录
                    zqb.insert_dayinterestlog('2015-07-31','2015-08-02',planexecution,plan)
                zqb.update_plannl()
            time.sleep(float(3))
        page+=1
        
batch()
