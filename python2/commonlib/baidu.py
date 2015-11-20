#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'c8d8z8@gmail.com'

import os
import sys
print os.name

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

#百度 配置
BDUSS_FILE = 'load.bduss'
SIGN_INTERVAL = 10

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
        print self.bduss
        
    def __paramparse__(self,param):
        # 将url上的参数 转换为dic
        print param
        str_arr = param.split('&')
        print str_arr
        body_data = {};
        for str in str_arr:
            temp_arr = str.split('=')
            body_data[temp_arr[0]]=temp_arr[1].encode('utf-8')
        print body_data
        return body_data
        
    def __readbduss__(self):
        #读取bduss信息
        if os.path.exists(os.path.join(cur_dir(),BDUSS_FILE)):
            print os.path.join(cur_dir(),BDUSS_FILE)
            
            with open(os.path.join(cur_dir(),BDUSS_FILE),'r') as f:
                # print type(f) # 注意系统变量 file
                bduss = f.read()
                return bduss
        return None
        
    def __writebduss__(self,bduss):
        # 写入bduss信息
        file_object = open(os.path.join(cur_dir(),BDUSS_FILE), 'w')
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
            bduss = None
        return self.bduss_login(bduss)
        
    def bduss_login(self,bduss):
        self.bduss = bduss
    
    def is_login(self):
        if not self.bduss:
            return False
        url='http://tieba.baidu.com/dc/common/tbs'
        data=http.request(url,cookie=self.bduss)
        k=json.loads(data)
        if k["is_login"]==1:
            return True
        else:
            return False
    
    def tieba_list(self):
        # 获取关注的贴吧列表
        url="http://c.tieba.baidu.com/c/f/forum/favolike"
        singbase= self.bduss +'&'+ client_id+'&'+ client_type+'&'+ client_version+'&'+ phone_imei+'&'+ net_type+'&'+ pn
        signmd5= self.bduss + client_id+ client_type+ client_version+ phone_imei+ net_type+ pn
        sign = '&sign=' + hashlib.md5((signmd5+'tiebaclient!!!').encode()).hexdigest()
        data=singbase+sign
        data=http.request(url,self.__paramparse__(data))
        tieba = []
        data=json.loads(data)
        list=data['forum_list']
        for x in list:
            tieba.append(x['name'].encode('gbk'))
        tbs='tbs='+data['anti']['tbs']
        return [tieba,tbs]
        
    def sign(self):
        tieba = self.tieba_list()
        url='http://c.tieba.baidu.com/c/c/forum/sign'
        tbs = tieba[1]
        for x in  tieba[0]:
            kw='kw='+x.decode('gbk')
            sign='&sign='
            signmd5= self.bduss + kw + tbs + 'tiebaclient!!!'
            signbase= self.bduss +'&'+ kw + '&' + tbs
            sign=sign+hashlib.md5(signmd5.encode('utf-8')).hexdigest()
            data=signbase+sign
            data=http.request(url,self.__paramparse__(data))
            data=json.loads(data)
            if data['error_code']=='0':
                print x , u'吧 签到成功！'
            else:
                print x , u'吧 签到失败！ 失败原因:' , data['error_msg'].encode('gbk')
            time.sleep(float(SIGN_INTERVAL))

def baiduUtf(data):
    datagb=data.decode("gbk")
    return urllib.quote_plus(datagb.encode('UTF-8'))
    #return urllib.parse.quote(datagb.encode('utf-8'))
    #return datagb
def cur_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

if __name__ == '__main__':
    tieba = BaiduTieba()
    if tieba.is_login():
        tieba.sign()
    
