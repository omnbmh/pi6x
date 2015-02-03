#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

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

def login(u,p):
    url = "http://zqbam.creditease.corp/pages/zqActiveUser/loginZqActiveUser.do"
    data = {'userCode':u,'userPassword':p}
    postData(url,data)
    # 获取用户信息
    url = "http://zqbam.creditease.corp/pages/zqUser/showZqUser.do"
    data = {'mobile':'18801182199','page':'1','rows':'20'}
    rt = postData(url,data)
    return json.loads(rt)
    
#修复计划执行状态
def fixplanexecution(pid,status):
    url = "http://zqbam.creditease.corp/pages/zqPlanexecution/showZqPlanexecution.do"
    data = {'pkPlanexexcution':pid,'page':'1','rows':'20'}
    rt = postData(url,data)
    jrt = json.loads(rt)
    logger.info('查询到计划执行' + str(jrt['total']) + '条')
    if (jrt['total'] >= 0):
        planexecution = jrt["rows"][0]
        logger.debug(planexecution)
        # 修改计划执行状态
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
    data = "fkPlan="+ planexecution['fkPalnexecutionPlan'] +"&page=1&rows=20&sort=pkLoanmoney&order=desc"
    rt = postData(url,data)
    jrt = json.loads(rt)
    logger.info('查询到总投资' + str(jrt['total']) + '条')
    if jrt['total'] <= 0: # 没有总投资
        # 增加一条总投资
        url = "http://zqbam.creditease.corp/pages/zqLoanmoney/addZqLoanmoney.do"
        data = "loanamount=" + planexecution["amount"] + "&invesetid=" + planexecution["investid"] + "&fkPlan=" + planexecution["fkPalnexecutionPlan"] + "&flag=0&createtime=&updatetime=&updateuser=&remark="
        rt = httpReady(url,data)
        logger.info('添加总投资结果'+rt)
        url = "http://zqbam.creditease.corp/pages/zqLoanmoney/showZqLoanmoney.do"
        data = "fkPlan=" +planexecution["fkPalnexecutionPlan"]+ "&page=1&rows=20&sort=pkLoanmoney&order=desc"
        rt = httpReady(url,data)
        jrt = json.loads(rt)
        #获得总投资信息
    loanmoney = jrt['rows'][0]
    return loanmoney
    
def fixloanmoneydet(pid,planexecution,loanmoney):
    #查询详细投资
    url = "http://zqbam.creditease.corp/pages/zqLoanmoneydet/showZqLoanmoneydet.do"
    data = "fkPlanexecution=" + pid + "&page=1&rows=20&sort=pkLoanmoneydet&order=desc"
    rt = httpReady(url,data)
    jrt = json.loads(rt)
    logger.info('查询到详细投资' + str(jrt['total']) + '条')
    if jrt['total'] <= 0: # 没有详细投资
        # 增加一条详细投资
        url =  "http://zqbam.creditease.corp/pages/zqLoanmoneydet/addZqLoanmoneydet.do"
        data = "fkLoanmoney="+loanmoney["pkLoanmoney"]+"&loanamount="+str(planexecution['amount'])+"&invesetid="+ loanmoney['invesetid']+"&fkPlanexecution="+pid+"&state=1&flag=0&cashierTime=2015-02-02+14%3A06%3A29&effectiveTime=2015-02-02+14%3A06%3A35&loanId=0&createtime=&updatetime=&updateuser=&remark=&addflag=1"
        rt = httpReady(url,data)
        logger.info('添加详细投资结果'+rt)
        
def fixdayinterestlog(planexecution):
    #更新收益
    paydate = planexecution['paysuccdate']
    paydate = datetime.datetime.strptime(paydate,'%Y%m%d')
    oneday = datetime.timedelta(days=1)
    interestdate = paydate + oneday
    
    #计算日收益 (amount*rate/365)*period
    num = float(str('%.2f'%(planexecution['amount'] * planexecution['rate'] / 365))) * planexecution['period']
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
    
def fixplan(pid):
    planexecution = fixplanexecution(pid,"0") # 0 成功
    if planexecution:
        #loanmoney = fixloanmoney(pid,planexecution)
        #fixloanmoneydet(pid,planexecution,loanmoney)
        fixdayinterestlog(planexecution)
        fixplannl(planexecution)
def batch():
    jrt = login('chendezhi','888888') # login
    if(jrt['total'] > 0):
        logger.info('登陆成功')
    else:
        logger.info('登陆失败')
        return
    #getData('http://zqbam.creditease.corp/pages/zqPlanexecution/toShowZqPlanexecution.do?pkActiveSysFunction=30041')
    logger.info('开始执行任务')
    for line in open("pid.txt"):
        pid = line.strip('\r\n')
        logger.info("执行任务 - 开始 - 计划执行 ID " + pid)
        fixplan(pid)
        logger.info("执行任务 - 结束 - 计划执行 ID " + pid)
    logger.info('结束执行任务')
    
batch()