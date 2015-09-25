#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

import os
print os.name
print os.path.abspath('.')

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

class BaiduTieba(object):
    
    def __init__(self):
        self.bduss = self.__readbduss__()
        
    def __paramparse__(self,param):
        # 将url上的参数 转换为dic
        print param
        str_arr = param.split('&')
        print str_arr
        body_data = {};
        for str in str_arr:
            temp_arr = str.split('=')
            body_data[temp_arr[0]]=temp_arr[1]
        print body_data
        return body_data
        
    def __readbduss__(self):
        #读取bduss信息
        flie=open(os.path.join(os.path.abspath('.'),'load.bduss'),'r')
        bduss=flie.read()
        flie.close()
        if islogin(bduss):
            return bduss
        else:
            nobduss()
            return
        
    def __writebduss__(self,bduss):
        # 写入bduss信息
        file_object = open('load.bduss', 'w')
        file_object.write(bduss)
        file_object.close()
        
    def toString(self):
        pass
        
    def login(self,acc,pwd):
        # login paramters
        pwd='passwd='+base64.b64encode(pwd.encode('utf-8')).decode()
        un="un="+baiduUtf(acc)
        signmd5= client_id+ client_type+ client_version+ phone_imei+pwd+un+ vcode_md5+"tiebaclient!!!"
        
        signbase= client_id+"&"+ client_type+'&'+ client_version+'&'+ phone_imei+'&'+pwd+'&'+un+'&'+ vcode_md5
        sign='&sign=' + hashlib.md5(signmd5.encode()).hexdigest()
        
        data=signbase+sign
        
        url='http://c.tieba.baidu.com/c/s/login'
        # start login
        data=http.request(url,self.__paramparse__(data))
        data=json.loads(data)
        
        if data['error_code']=='0':
            #login success & need save bduss
            bduss=data['user']['BDUSS'].encode('utf-8')
            bduss = 'BDUSS='+bduss.decode()
            self.__writebduss__(bduss)
        else:
            print data['error_msg']
            bduss = '123'
        return self.bduss_login(bduss)
        
    def bduss_login(self,bduss):
        self.bduss = bduss
        
    def tieba_list(self):
        # 获取关注的贴吧列表
        url="http://c.tieba.baidu.com/c/f/forum/favolike"
        singbase= bduss +'&'+ client_id+'&'+ client_type+'&'+ client_version+'&'+ phone_imei+'&'+ net_type+'&'+ pn
        signmd5= bduss + client_id+ client_type+ client_version+ phone_imei+ net_type+ pn
        sign = '&sign=' + hashlib.md5((signmd5+'tiebaclient!!!').encode()).hexdigest()
        data=singbase+sign
        data=http.request(url,self.__paramparse__(data))
        tieba = []
        data=json.loads(data)
        list=data['forum_list']
        for x in list:
            tieba.append(x['name'].encode('gbk'))
        tbs='tbs='+data['anti']['tbs']
        
    def sign(self):
        tieba = self.tieba_list()
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

def baiduUtf(data):
    datagb=data.decode("gbk")
    return urllib.quote_plus(datagb.encode('UTF-8'))
    #return urllib.parse.quote(datagb.encode('utf-8'))
    #return datagb



def islogin(bduss):
    url='http://tieba.baidu.com/dc/common/tbs'
    data=http.request(url,cookie=bduss)
    k=json.loads(data)
    if k["is_login"]==1:
        return True
    else:
        return False
    
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
    #auto_login()
    tieba = BaiduTieba()
    if not tieba.bduss:
        pass
        #tieba.login('deathwi','123456') #输出登陆状态
    