#!/usr/bin/python
# -*- coding: utf-8 -*-
# 更名 httpmylib.py httplib.py 系统中已经包含
# python 2.7 test passed

__author__ = 'c8d8z8@gmail.com'
'''
http 请求 支持cookie
'''
import urllib
import urllib2
import cookielib

#获取Cookiejar对象(存在本机的cookie信息)
cookie = cookielib.CookieJar()
#自定义opener,并将opener跟Cookiejar对象绑定
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#添加header emulate iphone 5s
opener.addheaders = [('User-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4')]

#安装opener,此后调用urlopen()时都会使用安装过的opener对象
urllib2.install_opener(opener)

import re
import hashlib
import json
import datetime
import os

def GET(url,data = None):
    if data:
        url = url + '?' + urllib.urlencode(data)
        print 'get param : %s' % urllib.urlencode(data)
    print 'get url : %s' % url
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req).read()
    print resp
    return resp

def request(url,data = None,cookie=None):
    print url
    print data
    if data:
        #将postdata转化成服务器编码的格式
        post_data = urllib.urlencode(data);
        req = urllib2.Request(url,post_data)
    else:
        req = urllib2.Request(url)

    #添加cookie
    if cookie:
        print cookie
        req.add_header('Cookie',cookie)

    resp = urllib2.urlopen(req).read()
    #print decode
    #resp = resp.decode(decode)
    print resp
    #print resp.status
    #print resp.encode(decode)

    #insert_req_to_musql(resp,url,post_data)
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
def cookies():
    return cookie

def test_request():
    url = 'https://www.itoumi.com/sxb/products/loans.json'
    data = {}
    data['url'] = 'products/loans.json'
    data['prodNo'] = '20150811163740805506'
    data['startId'] =  1
    data['maxRecords'] = 5

    rt = request(url,data)
    jrt = json.loads(rt)

    pass

if __name__ == '__main__':
    test_request()
    print urllib.urlencode({"username":"root","password":"ROOTXXOO"})
    print cookie
