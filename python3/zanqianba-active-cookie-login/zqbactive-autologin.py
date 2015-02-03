#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

#import md5
import hashlib
import base64
import json   
import time

import urllib.request
import urllib.parse
import http.cookiejar

# 让所有get和post请求都带上已经获取的cookie
cj = http.cookiejar.LWPCookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support , urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

def getData(url) :
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    return text
 
def postData(url, data) :
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'}
    # 这里的urlencode用于把一个请求对象用'&'来接来字符串化，接着就是编码成utf-8
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    return text
    
def login():
    url = "http://zqbam.creditease.corp/pages/zqActiveUser/loginZqActiveUser.do"
    data = {'userCode':'chendezhi','userPassword':'888888'}
    print(postData(url,data))
    # 获取用户信息
    url = "http://zqbam.creditease.corp/pages/zqUser/showZqUser.do"
    data = {'mobile':'18801182199','page':'1','rows':'20'}
    print(postData(url,data))
    
login()