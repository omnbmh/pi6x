#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

import json
import datetime
import math
import zqblib
jrt = zqblib.login()
    
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
