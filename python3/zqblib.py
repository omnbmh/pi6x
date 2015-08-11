1#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

'''
    登陆攒钱吧后台,并进行操作
    ZQB类 处理以计划为单位的问题
'''
# config logging
import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('zqb')
#logger.info('日志模块加载成功')

import hashlib
import base64
import json   
import time
import datetime
import math

import urllib.request
import urllib.parse
import http.cookiejar
# 让所有get和post请求都带上已经获取的cookie
cj = http.cookiejar.LWPCookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support , urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

#业务URL常量
import constant

def login(name,passwd):
    data = {'userCode':name,'userPassword':passwd}
    ZQB.request(constant.LOGIN,data)

class ZQB():
    
    def __init__(self,planid=None,planexecutionid=None):
        self.planid = planid
        self.planexecutionid = planexecutionid
        self.log_file = 'taskflow'
        if planid:
            self.log_file = self.log_file + '_p_' + planid
        if planexecutionid:
            self.log_file = self.log_file + '_pe_' + planexecutionid
        self.__id = self.log_file
        self.__logger = FileLogger('zqb.'+self.log_file,'logs/'+self.log_file+'.log')
        self.log_info('-- 执行任务 %s --' % self.__id)
        if planid:
            self.plan = self.select_plan(planid)
        if planexecutionid:
            self.planexecution = self.select_plan_execution_by_id(planexecutionid,None)
        
    def log_info(self, message):
        if self.__logger:
            self.__logger.info(message)
        else:
            logger.info(message)
    
    def request(url, data):
        logger.debug('url:'+url)
        logger.debug('data:'+json.dumps(data))
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'}
        # 这里的urlencode用于把一个请求对象用'&'来接来字符串化，接着就是编码成utf-8
        data = urllib.parse.urlencode(data).encode('utf-8')
        request = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(request)
        text = response.read().decode('utf-8')
        #log_info(text)
        return text
        
    def select_all_plan(self,page):
        '''
        查询计划详情
        '''
        data = {"planstate":0,"page":page,"rows":50,"sort":'pkPlan',"order":"desc"}
        # 调试参数
        #data['pkPlan'] = '5b5b38e7d20865e163a1df0c9af8364d'
        rt = ZQB.request('http://zqbam.creditease.corp/pages/zqPlan/showZqPlan.do',data);
        jrt = json.loads(rt)
        if jrt['total'] >0:
            self.log_info('查询到计划' + str(len(jrt['rows'])) + '条')
            return jrt['rows']
        return
        
    def select_plan(self,planid):
        '''
        查询计划详情
        '''
        data = {"pkPlan":planid,"page":1,"rows":20,"sort":'pkPlan',"order":"desc"}
        rt = ZQB.request('http://zqbam.creditease.corp/pages/zqPlan/showZqPlan.do',data);
        jrt = json.loads(rt)
        self.log_info('查询到计划' + str(jrt['total']) + '条')
        if jrt['total'] >0:
            return jrt['rows'][0]
        return
        
    def select_plan_execution_by_id(self,planexecutionid,state=None):
        '''
        查询计划的所有计划执行
        '''
        
        data = {'page':'1','state':state,'rows':'20',"sort":'period',"order":"asc"}
        if self.planid:
            data['fkPalnexecutionPlan'] = self.planid
            
        data['pkPlanexexcution'] = planexecutionid
        
        if state:
            data['state'] = state
        self.log_info(data)
        rt = ZQB.request(constant.SELECT_PLAN_EXECUTION,data)
        jrt = json.loads(rt)
        self.log_info('查询到计划执行' + str(jrt['total']) + '条')
        if (jrt['total'] > 0):
            return jrt["rows"][0]
        return
        
    def select_plan_execution(self,state):
        '''
        查询计划的所有计划执行
        '''
        data = {'fkPalnexecutionPlan':self.planid, 'page':'1','state':state,'rows':'20',"sort":'period',"order":"asc"}
        rt = ZQB.request(constant.SELECT_PLAN_EXECUTION,data)
        jrt = json.loads(rt)
        self.log_info('查询到计划执行' + str(jrt['total']) + '条')
        if (jrt['total'] > 0):
            return jrt["rows"]
        return
        
    def select_loanmoney(self):
        '''
        查询总投资
        '''
        url = "http://zqbam.creditease.corp/pages/zqLoanmoney/showZqLoanmoney.do"
        data = {"fkPlan":self.planid,"page":1,"rows":24,"sort":'pkLoanmoney',"order":"desc"}
        rt = ZQB.request(url,data)
        jrt = json.loads(rt)
        self.log_info('查询到总投资' + str(jrt['total']) + '条')
        if jrt['total'] > 0:
            return jrt['rows'][0]
        return 
    
    def select_loanmoneydet(self, planexecution):
        '''
        查询详细投资
        '''
        url = "http://zqbam.creditease.corp/pages/zqLoanmoneydet/showZqLoanmoneydet.do"
        data = {"fkPlanexecution":planexecution['pkPlanexexcution'],"page":1,"rows":20,"sort":'pkLoanmoneydet',"order":"desc"}
        rt = ZQB.request(url,data)
        jrt = json.loads(rt)
        if jrt['total'] > 0:
            self.log_info('查询到详细投资' + str(len(jrt['rows'])) + '条')
            return jrt['rows']
        return
    
    def insert_loanmoney(self,plan):
        # 增加一条总投资
        url = "http://zqbam.creditease.corp/pages/zqLoanmoney/addZqLoanmoney.do"
        data = {"loanamount":plan["principalamount"], "invesetid":plan["invesetid"],"fkPlan" : self.planid, "flag":0}
        rt = ZQB.request(url,data)
        self.log_info('添加总投资结果'+rt)
        return self.select_loanmoney(planid)
    
    def insert_loanmoneydet(self, planexecution, loanmoney, amount):
        # 增加一条详细投资
        self.log_info('添加详细投资金额 '+ str(amount))
        url =  "http://zqbam.creditease.corp/pages/zqLoanmoneydet/addZqLoanmoneydet.do"
        data = {"fkLoanmoney":loanmoney["pkLoanmoney"],"loanamount":str(amount),"invesetid":loanmoney['invesetid'],"fkPlanexecution":planexecution['pkPlanexexcution'],"state":1,"flag":0,"cashierTime":'2015-02-02 14:06:29',"effectiveTime":'2015-02-02 14:06:35','loanId':0,"addflag":1}
        rt = ZQB.request(url,data)
        self.log_info('添加详细投资结果'+rt)
        return self.select_loanmoneydet(planexecution)
    
    def insert_planexecution(self,planexecution,status):
        '''
        增加计划执行状态 
        默认 8 支付失败
        '''
        if (planexecution):
            url = "http://zqbam.creditease.corp/pages/zqPlanexecution/addZqPlanexecution.do"
            data = {"pkPlanexexcution":planexecution['pkPlanexexcution'],"state":status}
            rt = ZQB.request(url,data)
            self.log_info('修改计划执行状态结果'+rt)
            self.planexecutionid=planexecution['pkPlanexexcution']
            return self.select_plan_execution(0)
        else:
            return
    
    def update_planexecution(self,planexecution,status):
        '''
        修改计划执行状态 
        0 成功
        8 支付失败
        '''
        if (planexecution):
            url = "http://zqbam.creditease.corp/pages/zqPlanexecution/modZqPlanexecution.do"
            data = {"pkPlanexexcution":planexecution['pkPlanexexcution'],"state":status}
            rt = ZQB.request(url,data)
            self.log_info('修改计划执行状态结果'+rt)
            self.planexecutionid=planexecution['pkPlanexexcution']
            return self.select_plan_execution(0)
        else:
            return
            
    def select_dayinterestlog(self, plan):
        data = {"planid":plan['pkPlan'],"page":1,"rows":20,"sort":'interestdate',"order":"asc"}
        rt = ZQB.request('http://zqbam.creditease.corp/pages/zqDayinterestlog/showZqDayinterestlog.do',data)
        
        jrt = json.loads(rt)
        if (jrt['total'] > 0):
            return jrt["rows"]
        return
    
    def insert_dayinterestlog(self, start_date,end_date,planexecution,plan):
        '''
        新增每日收益
        '''
        
        #计算日收益 (amount*rate/365)*period  # math.ceil(round(500 * 0.1 / 365,3)*100)/100
        num = math.ceil(round(planexecution['amount'] * planexecution['rate'] / 365,3)*100)/100*plan['alreadyperiod']
        data = {'planid':planexecution['fkPalnexecutionPlan'],'dayamont':num,'createtime':start_date,'updatetime':end_date}
        rt = ZQB.request('http://zqbam.creditease.corp/pages/zqDayinterestlog/addZqDayinterestlog.do',data)
        self.log_info('增加收益结果'+rt)
    
    def update_dayinterestlog(self, planexecution,next_planexecution,times):
        '''
        只修改最新一期支付成功的收益
        param times 已成功投资多少次 截至 当前要修改的计划执行
        '''
        oneday = datetime.timedelta(days=1)
        
        paydate = planexecution['paysuccdate']
        paydate = datetime.datetime.strptime(paydate,'%Y%m%d')
        paydate = paydate + oneday
        if next_planexecution:
            next_paydate = next_planexecution['paysuccdate']
            next_paydate = datetime.datetime.strptime(next_paydate,'%Y%m%d')
            next_paydate = next_paydate + oneday
        else:
            next_paydate = datetime.datetime.now()
        
        #计算日收益 (amount*rate/365)*period  # math.ceil(round(500 * 0.1 / 365,3)*100)/100
        num = math.ceil(round(planexecution['amount'] * planexecution['rate'] / 365,3)*100)/100*times
        data = {'planid':planexecution['fkPalnexecutionPlan'],'dayamont':num,'createtime':paydate.strftime('%Y-%m-%d'),'updatetime':next_paydate.strftime('%Y-%m-%d')}
        rt = ZQB.request('http://zqbam.creditease.corp/pages/zqDayinterestlog/modZqDayinterestlogBatch.do',data)
        self.log_info('修改日收益结果'+rt)
        
    def update_plannl(self):
        #查询日收益
        data={'planid':self.planid,'page':1,'rows':760}
        rt = ZQB.request('http://zqbam.creditease.corp/pages/zqDayinterestlog/showZqDayinterestlog.do',data)
        jrt = json.loads(rt)
        if (jrt['total'] > 0):
            tnum = 0
            for j in jrt['rows']:
                tnum += j['dayamont']
            data = {'pkPlan':self.planid,'interestamountnl':tnum}
            rt = ZQB.request('http://zqbam.creditease.corp/pages/zqPlan/modZqPlan.do',data)
            self.log_info('修改计划界面收益结果'+rt)
        
class FileLogger():
    def __init__(self, name, file):
        self.__logger = logging.getLogger(name)
        handler = logging.FileHandler(file)
        fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(fmt)
        self.__logger.addHandler(handler)
        
    def info(self, message):
        if self.__logger is not None:
            self.__logger.info(message)
            
            