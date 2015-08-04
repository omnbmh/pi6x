#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

# config logging
import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('zqb')

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
        zqb.update_plannl()
        
batch()
