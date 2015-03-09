#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

'''
    本程序主要用于批量修复用户的收益
    仅修复执行执行状态为成功的计划执行的收益 计划执行状态不对的请先修复计划执行的状态
'''

# config logging
import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('zqb')
logger.info('日志模块加载成功')

import urllib.request
import urllib.parse
import http.cookiejar

# 让所有get和post请求都带上已经获取的cookie
cj = http.cookiejar.LWPCookieJar()
#cj = http.cookiejar.FileCookieJar('zqb.cookies')
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support , urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

def getData(url) :
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    logger.debug(text)
    return text
 
def postData(url, data) :
    logger.debug('url:'+url)
    logger.debug('data:'+json.dumps(data))
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'}
    # 这里的urlencode用于把一个请求对象用'&'来接来字符串化，接着就是编码成utf-8
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    logger.debug(text)
    return text
    
import json
import datetime
import math

def login(u,p):
    url = "http://zqbam.creditease.corp/pages/zqActiveUser/loginZqActiveUser.do"
    data = {'userCode':u,'userPassword':p}
    postData(url,data)
    # 获取用户信息
    url = "http://zqbam.creditease.corp/pages/zqUser/showZqUser.do"
    data = {'mobile':'18801182199','page':'1','rows':'20'}
    rt = postData(url,data)
    return json.loads(rt)
    
def fixplanexecution(pid,status):
    '''
    修改计划执行状态 
    0 成功
    8 支付失败
    '''
    url = "http://zqbam.creditease.corp/pages/zqPlanexecution/showZqPlanexecution.do"
    data = {'pkPlanexexcution':pid,'page':'1','rows':'20'}
    rt = postData(url,data)
    jrt = json.loads(rt)
    logger.info('查询到计划执行' + str(jrt['total']) + '条')
    if (jrt['total'] >= 0):
        planexecution = jrt["rows"][0]
        logger.debug(planexecution)
        url = "http://zqbam.creditease.corp/pages/zqPlanexecution/modZqPlanexecution.do"
        data = {"pkPlanexexcution":pid,"state":status}
        rt = postData(url,data)
        logger.info('修改计划执行状态结果'+rt)
        return planexecution
    else:
        return
    
def fixloanmoney(pid,planexecution):
    # 查询总投资
    url = "http://zqbam.creditease.corp/pages/zqLoanmoney/showZqLoanmoney.do"
    data = {"fkPlan":planexecution['fkPalnexecutionPlan'],"page":1,"rows":20,"sort":'pkLoanmoney',"order":"desc"}
    rt = postData(url,data)
    jrt = json.loads(rt)
    logger.info('查询到总投资' + str(jrt['total']) + '条')
    if jrt['total'] <= 0: # 没有总投资
        # 增加一条总投资
        url = "http://zqbam.creditease.corp/pages/zqLoanmoney/addZqLoanmoney.do"
        data = {"loanamount":planexecution["amount"], "invesetid":planexecution["investid"],"fkPlan" : planexecution["fkPalnexecutionPlan"], "flag":0}
        rt = postData(url,data)
        logger.info('添加总投资结果'+rt)
        url = "http://zqbam.creditease.corp/pages/zqLoanmoney/showZqLoanmoney.do"
        data = {"fkPlan":planexecution['fkPalnexecutionPlan'],"page":1,"rows":20,"sort":'pkLoanmoney',"order":"desc"}
        rt = postData(url,data)
        jrt = json.loads(rt)
        #获得总投资信息
    loanmoney = jrt['rows'][0]
    return loanmoney
    
def fixloanmoneydet(pid,planexecution,loanmoney):
    #查询详细投资
    url = "http://zqbam.creditease.corp/pages/zqLoanmoneydet/showZqLoanmoneydet.do"
    data = {"fkPlanexecution":pid,"page":1,"rows":20,"sort":'pkLoanmoneydet',"order":"desc"}
    rt = postData(url,data)
    jrt = json.loads(rt)
    logger.info('查询到详细投资' + str(jrt['total']) + '条')
    if jrt['total'] <= 0: # 没有详细投资
        # 增加一条详细投资
        url =  "http://zqbam.creditease.corp/pages/zqLoanmoneydet/addZqLoanmoneydet.do"
        data = {"fkLoanmoney":loanmoney["pkLoanmoney"],"loanamount":str(planexecution['amount']),"invesetid":loanmoney['invesetid'],"fkPlanexecution":pid,"state":1,"flag":0,"cashierTime":'2015-02-02 14:06:29',"effectiveTime":'2015-02-02 14:06:35','loanId':0,"addflag":1}
        rt = postData(url,data)
        logger.info('添加详细投资结果'+rt)
        
def fixdayinterestlog(planexecution,plan):
    #更新收益
    paydate = planexecution['paysuccdate']
    paydate = datetime.datetime.strptime(paydate,'%Y%m%d')
    oneday = datetime.timedelta(days=1)
    interestdate = paydate + oneday
    
    #计算日收益 (amount*rate/365)*period  # math.ceil(round(500 * 0.1 / 365,3)*100)/100
    num = math.ceil(round(planexecution['amount'] * planexecution['rate'] / 365,3)*100)/100*plan['alreadyperiod']
    data = {'planid':planexecution['fkPalnexecutionPlan'],'dayamont':num,'createtime':interestdate.strftime('%Y-%m-%d'),'updatetime':datetime.datetime.now().strftime('%Y-%m-%d')}
    rt = postData('http://zqbam.creditease.corp/pages/zqDayinterestlog/modZqDayinterestlogBatch.do',data)
    logger.info('修改收益结果'+rt)

# 修改界面收益    
def fixplannl(planexecution):
    #查询日收益
    data={'planid':planexecution['fkPalnexecutionPlan'],'page':1,'rows':760}
    rt = postData('http://zqbam.creditease.corp/pages/zqDayinterestlog/showZqDayinterestlog.do',data)
    jrt = json.loads(rt)
    if (jrt['total'] > 0):
        tnum = 0
        for j in jrt['rows']:
            tnum += j['dayamont']
        data = {'pkPlan':planexecution['fkPalnexecutionPlan'],'interestamountnl':tnum}
        rt = postData('http://zqbam.creditease.corp/pages/zqPlan/modZqPlan.do',data)
        logger.info('修改计划界面收益结果'+rt)
        
def searchplan(planid):
    '''
    查询计划信息
    '''
    data = {"pkPlan":planid,"page":1,"rows":20,"sort":'pkPlan',"order":"desc"}
    rt = postData('http://zqbam.creditease.corp/pages/zqPlan/showZqPlan.do',data);
    jrt = json.loads(rt)
    if (jrt['total'] > 0):
        plan = jrt['rows'][0]
        return plan
    return
    
def searchplanexecution(planid):
    url = "http://zqbam.creditease.corp/pages/zqPlanexecution/showZqPlanexecution.do"
    data = {'pkPlanexexcution':pid,'page':'1','rows':'20'}
    rt = postData(url,data)
    jrt = json.loads(rt)
    logger.info('查询到计划执行' + str(jrt['total']) + '条')
    if (jrt['total'] >= 0):
        return
    return None
        
def fixplan(planid):
    '''
    修复有问题的计划
    '''
    plan = searchplan(planid)
    if plan:
        planexecution = fixplanexecution(pid,"0")
        loanmoney = fixloanmoney(pid,planexecution)
        fixloanmoneydet(pid,planexecution,loanmoney)
        fixdayinterestlog(planexecution,plan)
        fixplannl(planexecution)
    
def batch():
    '''
    读取planid.txt文件 获得计划id 批量执行
    '''
    jrt = login('chendezhi','888888')
    if(jrt['total'] > 0):
        logger.info('登陆成功')
    else:
        logger.info('登陆失败')
        return
    #getData('http://zqbam.creditease.corp/pages/zqPlanexecution/toShowZqPlanexecution.do?pkActiveSysFunction=30041')
    logger.info('开始执行任务')
    for line in open("planid.txt"):
        planid = line.strip('\r\n')
        logger.info("执行任务 - 开始 - 计划 ID " + planid)
        fixplan(planid)
        logger.info("执行任务 - 结束 - 计划 ID " + planid)
    logger.info('结束执行任务')
    
batch()
