#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'c8d8z8@gmail.com'

import urllib
import urllib2
import cookielib

#获取Cookiejar对象(存在本机的cookie信息)
cookie = cookielib.CookieJar()
#自定义opener,并将opener跟Cookiejar对象绑定
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#安装opener,此后调用urlopen()时都会使用安装过的opener对象
urllib2.install_opener(opener)
#添加header emulate iphone 5s
opener.addheaders = [('User-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4')]
    
import re
import hashlib
import json

import os
    
def request(url,data = None,cookie=None,decode='raw_unicode_escape'):

    if data:
        #将postdata转化成服务器编码的格式
        post_data = urllib.urlencode(data);
        req = urllib2.Request(url,post_data)
    else:
        req = urllib2.Request(url)
        
    #添加cookie
    if cookie:
        req.add_header('Cookie',cookie) 
    
    resp = urllib2.urlopen(req).read()
    #print decode
    #resp = resp.decode(decode)
    #print resp.status
    #print resp.encode(decode)
    return resp

def download(url,fpath,fname):
    print fpath+fname 
    try:
        if not os.path.exists(fpath):
            os.makedirs(fpath)
    except Exception as e:
        print e
        print u'path not found!'
        exit()
        
    data = urllib.urlopen(url).read()
    
    f = file(fpath+fname,'wb')
    f.write(data)
    f.close()
    print 'download file complete - save as ' + fpath+fname
    
def paramparse(param):
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
    
def test_request():
    request('https://www.baidu.com/s',{'wd':'python'},None)
    request('https://www.baidu.com',None,None)
    
if __name__ == '__main__':
    test_request()
    
