#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

import urllib.request
#import md5
import hashlib
import base64
import json   
import time
import urllib.parse

jsessionid = '98CC83D72B35EF673DC7C7300EFA3743'

def httpReady(url,data=None,cookie="JSESSIONID=" + jsessionid):
    print(url)
    print(data)
    print(cookie)
    #request url
    if data:
        req=urllib.request.Request(url,data.encode('utf-8'))
    else:
        req=urllib.request.Request(url)
    #add cookie
    if cookie:
        req.add_header('Cookie',cookie)    
    #emulate chrome
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    req.add_header('Cache-Control','no-cache')
    v=urllib.request.urlopen(req).read().decode('utf-8')
    print(v)
    return v
    
def login():
    url = "http://zqbam.creditease.corp/zqbactive/pages/zqUser/showZqUser.do"
    data = "page=1&rows=20&sort=pkUser&order=desc"
    #cookie = "JSESSIONID=" + jsessionid
    print(httpReady(url,data))
    

def updatePlanexecutionStatus(pid,s):
    url = "http://zqbam.creditease.corp/zqbactive/pages/zqPlanexecution/showZqPlanexecution.do"
    data = "pkPlanexexcution="+pid+"&page=1&rows=20&sort=pkPlanexexcution&order=desc"
    rt = httpReady(url,data)
    jrt = json.loads(rt)

    planexecution = jrt["rows"][0]
    print(planexecution)
    
    # 更新计划执行状态
    url = "http://zqbam.creditease.corp/zqbactive/pages/zqPlanexecution/modZqPlanexecution.do"
    data = "pkPlanexexcution="+pid+"&state="+s
    httpReady(url,data)
    return planexecution

def fixloanmoney(pid,planexecution):
    # 查询总投资
    url = "http://zqbam.creditease.corp/zqbactive/pages/zqLoanmoney/showZqLoanmoney.do"
    data = "fkPlan="+ planexecution['fkPalnexecutionPlan'] +"&page=1&rows=20&sort=pkLoanmoney&order=desc"
    rt = httpReady(url,data)
    jrt = json.loads(rt)
    print(jrt)
    if jrt['total'] <= 0: # 没有总投资
        # 增加一条总投资
        url = "http://zqbam.creditease.corp/zqbactive/pages/zqLoanmoney/addZqLoanmoney.do"
        data = "loanamount=" + planexecution["amount"] + "&invesetid=" + planexecution["investid"] + "&fkPlan=" + planexecution["fkPalnexecutionPlan"] + "&flag=0&createtime=&updatetime=&updateuser=&remark="
        rt = httpReady(url,data)
        url = "http://zqbam.creditease.corp/zqbactive/pages/zqLoanmoney/showZqLoanmoney.do"
        data = "fkPlan=" +planexecution["fkPalnexecutionPlan"]+ "&page=1&rows=20&sort=pkLoanmoney&order=desc"
        rt = httpReady(url,data)
        jrt = json.loads(rt)
        print(jrt)
    #获得总投资信息
    loanmoney = jrt['rows'][0]

    url = "http://zqbam.creditease.corp/zqbactive/pages/zqLoanmoneydet/showZqLoanmoneydet.do"
    data = "fkPlanexecution=" + pid + "&page=1&rows=20&sort=pkLoanmoneydet&order=desc"
    rt = httpReady(url,data)
    jrt = json.loads(rt)
    print(jrt)
    if jrt['total'] <= 0: # 没有详细投资
        # 添加详细投资
        url =  "http://zqbam.creditease.corp/zqbactive/pages/zqLoanmoneydet/addZqLoanmoneydet.do"
        data = "fkLoanmoney="+loanmoney["pkLoanmoney"]+"&loanamount="+str(planexecution['amount'])+"&invesetid="+ loanmoney['invesetid']+"&fkPlanexecution="+pid+"&state=1&flag=0&cashierTime=2015-02-02+14%3A06%3A29&effectiveTime=2015-02-02+14%3A06%3A35&loanId=0&createtime=&updatetime=&updateuser=&remark=&addflag=1"
        rt = httpReady(url,data)
        jrt = json.loads(rt)
        print(jrt)
    else:
        print(jrt)
#login()
#fixloanmoney('8b5d68f42113d0fdfeaf26dbf36ac960');
#updatePlanexecutionStatus("88b7700d6f2a4703c7ed466868a940c3","12")

def batch():
    for line in open("pid.txt"):
        line = line.strip('\r\n')
        print("----------" + line + "--------------------")
        planexecution = updatePlanexecutionStatus(line,"0") # 投资成功
        fixloanmoney(line,planexecution)
        print("-----------------------------------------")
batch()


#修改计划执行投资处理中 支付成功 已经成功投资的
# 需要参数 投资id 计划执行id 计划id
