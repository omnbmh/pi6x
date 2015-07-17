1#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

'''
    带Cookie的网络请求工具类
'''
import hashlib
import base64
import json   
import time
import datetime
import math

import urllib.request
import urllib.parse
import http.cookiejar

# 让所有get和post请求都带上已经获取的cookie
cj = http.cookiejar.LWPCookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support , urllib.request.HTTPHandler)
urllib.request.install_opener(opener)

def request(url, data):
	#logger.debug('url:'+url)
	#logger.debug('data:'+json.dumps(data))
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'}
	# 这里的urlencode用于把一个请求对象用'&'来接来字符串化，接着就是编码成utf-8
	data = urllib.parse.urlencode(data).encode('utf-8')
	request = urllib.request.Request(url, data, headers)
	response = urllib.request.urlopen(request)
	text = response.read().decode('utf-8')
	return text
    
def getData(url) :
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    return text