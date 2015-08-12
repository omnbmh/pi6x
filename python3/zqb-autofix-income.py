#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

'''
    本程序主要用于批量修复用户的收益
    仅修复执行执行状态为成功的计划执行的收益
    计划执行状态不对的请先修复计划执行的状态
'''

import json
import datetime
import math
import zqblib
import time

zqblib.login()
    
def batch():
    '''
    读取planid.txt文件 获得计划id 批量执行
    '''
    print('执行任务开始')
    for line in open("planid.txt"):
        planid = line.strip('\r\n')
        zqb = zqblib.ZQB(planid)
        # 根据状态 查询 计划执行 0 成功
        planexecutions = zqb.select_plan_execution(0)
        if zqb.plan and planexecutions:
            for i in range(0,len(planexecutions)):
                #只修复最近五期的收益
                if(i>24):
                    break
                cur_pe = planexecutions[i]
                next_pe = None if i == 0 else planexecutions[i-1]
                loanmoney = zqb.select_loanmoney()
                if not loanmoney:
                    loanmoney = zqb.insert_loanmoney(zqb.plan)
                loanmoneydets = zqb.select_loanmoneydet(cur_pe)
                if not loanmoneydets:
                    zqb.insert_loanmoneydet(cur_pe,loanmoney, cur_pe['amount'])
                else:
                    # 需要补的收益
                    amount = 0;
                    for l in loanmoneydets:
                        amount = amount + l['loanamount'];
                    if amount < cur_pe['amount']:
                        print('已记录金额：'+str(amount))
                        amount = cur_pe['amount'] - amount
                        # 保留两位小数
                        amount = math.ceil(amount*100)/100
                        zqb.insert_loanmoneydet(cur_pe,loanmoney, amount)
                        print('记录总金额：'+str(cur_pe['amount'])+' 需要补金额：'+str(amount) + '')
                zqb.update_dayinterestlog(cur_pe,next_pe,len(planexecutions) - i)
            # 更新界面总收益
            tnum = zqb.count_plannl()
            zqb.plan['principalamount'] = zqb.plan['monthinvestmentamount'] * len(planexecutions)
            #查询全部的计划执行
            pes = zqb.select_plan_execution(0)
            zqb.plan['nowperiod'] = len(pes) + 1
            zqb.plan['alreadyperiod'] = len(planexecutions)
            zqb.plan['interestamountnl'] = tnum
            zqb.update_plan(zqb.plan)
        #执行每个计划间隔50ms
        time.sleep(float(50))        
    print('执行任务结束')
    
batch()
