#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

# 以下4行代码说简单点就是让你接下来的所有get和post请求都带上已经获取的cookie，因为稍大些的网站的登陆验证全靠cookie
cj = http.cookiejar.LWPCookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support , urllib.request.HTTPHandler)
urllib.request.install_opener(opener)
 
# 封装一个用于get的函数，新浪微博这边get出来的内容编码都是-8，所以把utf-8写死在里边了，真实项目中建议根据内容实际编码来决定
def getData(url) :
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    return text
    
# 封装一个用于post的函数，验证密码和用户名都是post的，所以这个postData在本demo中专门用于验证用户名和密码
def postData(url , data) :
    # headers需要我们自己来模拟
    headers = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
    # 这里的urlencode用于把一个请求对象用'&'来接来字符串化，接着就是编码成utf-8
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url , data , headers)
    response = urllib.request.urlopen(request)
    text = response.read().decode('gbk')
    return text
    
def login():
    