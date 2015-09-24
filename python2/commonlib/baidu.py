#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com
'''
    百度
    百度贴吧自动签到
'''
import urllib
import http
#import md5
import hashlib
import base64
import json
import time

# baidu login http request paramters
client_id='_client_id=wappc_1368589871859_564'
client_type='_client_type=2'
client_version='_client_version=2.0.3'
phone_imei='_phone_imei='
net_type='net_type=3'
vcode_md5='vcode_md5='
pn='pn=1'

def bdussFile():
    if not base_dir:
        return 'load.bduss'
    return base_dir + '/' + 'load.bduss'

def baiduUtf(data):
    datagb=data.decode("gbk")
    return urllib.quote_plus(datagb.encode('UTF-8'))
    #return urllib.parse.quote(datagb.encode('utf-8'))
    #return datagb

def readbduss():
    #read bduss file
    try:
        flie=open(bdussFile(),'r')
        bduss=flie.read()
        flie.close()
        if islogin(bduss):
            return bduss
        else:
            logger.warning('没有发现bduss文件')
            nobduss()
            return
    except:
        return
        
def writebduss(bduss):
    # write bduss file
    file_object = open(bdussFile(), 'w')
    file_object.write(bduss)
    file_object.close()

def islogin(bduss):
    url='http://tieba.baidu.com/dc/common/tbs'
    data=http.request(url,cookie=bduss)
    k=json.loads(data)
    if k["is_login"]==1:
        return True
    else:
        return False
def sign(bduss):
    # get tieba list
    url="http://c.tieba.baidu.com/c/f/forum/favolike"
    singbase= bduss +'&'+ client_id+'&'+ client_type+'&'+ client_version+'&'+ phone_imei+'&'+ net_type+'&'+ pn
    signmd5= bduss + client_id+ client_type+ client_version+ phone_imei+ net_type+ pn
    sign = '&sign=' + hashlib.md5((signmd5+'tiebaclient!!!').encode()).hexdigest()
    data=singbase+sign
    data=http.request(url,data)
    tieba = []
    data=json.loads(data)
    list=data['forum_list']
    for x in list:
        tieba.append(x['name'].encode('gbk'))
    tbs='tbs='+data['anti']['tbs']
    
    
    url='http://c.tieba.baidu.com/c/c/forum/sign'
    for x in  tieba:
        kw='kw='+x.decode('gbk')
        sign='&sign='
        signmd5= bduss + kw + tbs + 'tiebaclient!!!'
        signbase= bduss +'&'+ kw + '&' + tbs
        sign=sign+hashlib.md5(signmd5.encode('utf-8')).hexdigest()
        data=signbase+sign
        data=http.request(url,data)
        data=json.loads(data)
        if data['error_code']=='0':
            logger.info(x.decode('gbk') + '吧 签到成功！')
        else:
            logger.info(x.decode('gbk') + '吧 签到失败！ 失败原因:' + data['error_msg'])
        time.sleep(float(interval))
    return
    
def namepwd_login(user=None, password=None):
    # login paramters
    
    password='passwd='+base64.b64encode(password.encode('utf-8')).decode()
    un="un="+baiduUtf(user)
    signmd5= client_id+ client_type+ client_version+ phone_imei+password+un+ vcode_md5+"tiebaclient!!!"
    
    signbase= client_id+"&"+ client_type+'&'+ client_version+'&'+ phone_imei+'&'+password+'&'+un+'&'+ vcode_md5
    sign='&sign=' + hashlib.md5(signmd5.encode()).hexdigest()
    
    data=signbase+sign
    url='http://c.tieba.baidu.com/c/s/login'
    # start login
    data=http.request(url,data)
    data=json.loads(data)
    
    if data['error_code']=='0':
        #login success & need save bduss
        bduss=data['user']['BDUSS'].encode('utf-8')
        bduss = 'BDUSS='+bduss.decode()
        writebduss(bduss)

    return bduss
    
def auto_login():
    bduss=readbduss()
    if bduss:
        sign(bduss)
    else:
        user= 'deathwingo' #input('请输入账号:')
        password= '123456' #input('请输入密码:')
        bduss = namepwd_login(user,password)
        sign(bduss)
if __name__ == '__main__':
    auto_login()