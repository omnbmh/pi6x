#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import lib
import urllib.request
#import md5
import hashlib
import base64
import json
import time
import json
import urllib.parse

def httpReady(url,data=None,cookie=None):
    #request url
    if data:
        req=urllib.request.Request(url,data.encode('utf-8'))
    else:
        req=urllib.request.Request(url)
    #add cookie
    if cookie:
        req.add_header('Cookie',cookie)    
    #emulate iphone 5s
    req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53')
    v=urllib.request.urlopen(req).read().decode('raw_unicode_escape')
    return v


def baiduUtf(data):
    datagb=data#.decode("gbk")
    #return urllib.quote_plus(datagb.encode('UTF-8'))
    return urllib.parse.quote(datagb.encode('utf-8'))


class Account:
    client_id='_client_id=wappc_1368589871859_564'
    client_type='_client_type=2'
    client_version='_client_version=2.0.3'
    phone_imei='_phone_imei='
    net_type='net_type=3'
    vcode_md5='vcode_md5='
    pn='pn=1'
    tieba=[]
    def __init__(self,user=None,password=None,bduss=None):
        if bduss:
            self.bduss=bduss
            if user:
                self.user=user
            else:
                self.user=''
        else:
            self.user=user
            self.password=password
            self.login()
            
    def login(self):
        # login func
        sign='&sign='
        print(self.password)
        password='passwd='+base64.b64encode(self.password.encode('utf-8')).decode()
        un="un="+baiduUtf(self.user)
        signmd5=self.client_id+self.client_type+self.client_version+self.phone_imei+password+un+self.vcode_md5+"tiebaclient!!!"
        signbase=self.client_id+"&"+self.client_type+'&'+self.client_version+'&'+self.phone_imei+'&'+password+'&'+un+'&'+self.vcode_md5
        sign=sign+hashlib.md5(signmd5.encode()).hexdigest()
        data=signbase+sign
        url='http://c.tieba.baidu.com/c/s/login'
        data=httpReady(url,data)
        self.loginsplit(data)
        return
    
    def loginsplit(self,logindata):
        data=json.loads(logindata)
        if data['error_code']=='0':
                bduss=data['user']['BDUSS'].encode('utf-8')
                self.bduss='BDUSS='+bduss.decode()
                self.writebduss()
                print(time.ctime(),self.user,'write bduss ok!')
                return
        else:
            print(data)
            print(time.ctime(), self.user,data['error_msg'])
            return
        
    def like(self):
        url="http://c.tieba.baidu.com/c/f/forum/favolike"
        sign='&sign='
        singbase=self.bduss+'&'+self.client_id+'&'+self.client_type+'&'+self.client_version+'&'+self.phone_imei+'&'+self.net_type+'&'+self.pn
        signmd5=self.bduss+self.client_id+self.client_type+self.client_version+self.phone_imei+self.net_type+self.pn
        sign=sign+hashlib.md5((signmd5+'tiebaclient!!!').encode()).hexdigest()
        data=singbase+sign
        data=httpReady(url,data)
        self.likesplit(data)
        return
    
    def likesplit(self,likedata):
        data=json.loads(likedata)
        list=data['forum_list']
        for x in list:
            self.tieba.append(x['name'].encode('gbk'))
        self.tbs='tbs='+data['anti']['tbs']#.encode('utf-8')
        return
    
    def sign(self):
        self.like()
        url='http://c.tieba.baidu.com/c/c/forum/sign'
        for x in self.tieba:
            kw='kw='+x.decode('gbk')
            sign='&sign='
            signmd5=self.bduss+kw+self.tbs+'tiebaclient!!!'
            signbase=self.bduss+'&'+kw+'&'+self.tbs
            sign=sign+hashlib.md5(signmd5.encode('utf-8')).hexdigest()
            data=signbase+sign
            data=httpReady(url,data)
            self.signsplit(data,x)
            time.sleep(2)
        return
    
    def signsplit(self,signdata,x):
        data=json.loads(signdata)
        if data['error_code']=='0':
            print(time.ctime(), self.user,x,data['user_info'])
        else:
            print(time.ctime(), self.user,x,data['error_msg'])

    def writebduss(self):
        file_object = open('load.bduss', 'w')
        file_object.write(self.bduss)
        file_object.close()



def readbduss():
    try:
        flie=open('load.bduss','r')
        bduss=flie.read()
        flie.close()
        if islogin(bduss):
            return bduss
        else:
            print('没有发现bduss文件')
            nobduss()
            return
    except:
        return
def star():
    ss=input('请输入百度账号密码')
    if ss.upper()=='Y'or ss=='y':
        autobduss()
    elif ss.upper()=='N':
        nobduss()
    else:
        print('账号。密码')
        star()
        
def nobduss():
    user=input('账号:')
    password=input('密码:')
    print(user, password)
    aa=Account(user,password)
    if aa.bduss:
        aa.sign()
    else:
        nobduss()

    
def autobduss():
    bduss=readbduss()
    if bduss:
        aa=Account(bduss=bduss)
        print('加载 bduss')
        aa.sign()
    else:
        print('bduss')
        nobduss()

def islogin(bduss):
    url='http://tieba.baidu.com/dc/common/tbs'
    data=httpReady(url,cookie=bduss)
    k=json.loads(data)
    if k["is_login"]==1:
        return True
    else:
        return False
    
autobduss()
