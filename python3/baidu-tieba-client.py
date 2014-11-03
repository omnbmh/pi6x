#!/usr/bin/python3
#-*- coding=utf-8 -*-

# html parser
from html.parser import HTMLParser
class TieBaParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tieBaList = list()
        self.flag = False
    def get_tieba_list(self):
        return self.tieBaList

    def handle_start_tag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and "m?kw=" in value:
                    self.flag = True

    def handle_data(self, data):
        if self.flag:
            self.tieBaList.append(data)
            self.flag = False

# http util
def get_cookies_from_headers(headers):
    cookies = list()
    for header in headers:
        if "set-Cookie" in header:
            cookie = header[1].split(";")[0]
            cookies.append(cookie)
    return cookies

def save_cookies(headers, cookies):
    for cookie in cookies:
        headers["Cooike"] += cookie + ";"

def get_cookie_value(cookies, cookieName):
    for cookie in cookies:
        if cookieName in cookie:
            index = cookie.index("=") + 1
            value = cookie[index:]
            return value

def parser_query_string(queryString):
    result = dict()
    strs = queryString.split("&")
    for s in strs:
        name = s.split("=")[0]
        value = s.split("=")[1]
        result[name] = value
    return result

# tieba client
import urllib.parse
import gzip
import json
import re
from http.client import HTTPConnection

headers = dict()
headers["Connection"] = "keep-alive"
headers["Cache-Control"] = "max-age=0"
headers["Accept"] = "*/*"
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"
#headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Accept-Encoding"] = "gzip,deflate,sdch"
headers["Accept-Language"] = "zh-CN,zh;q=0.8"
headers["Cookie"] = ""

cookies = list()

userinfo = {}

def login(account, password):
    global cookies
    headers["Host"] = "wappass.baidu.com"
    body = "username={0}&password={1}&submit=%E7%99%BB%E5%BD%95&quick_user=0&isphone=0&sp_login=waprate&uname_login=&loginmerge=1&vcodestr=&u=http%253A%252F%252Fwap.baidu.com%253Fuid%253D1392873796936_247&skin=default_v2&tpl=&ssid=&from=&uid=1392873796936_247&pu=&tn=&bdcm=3f7d51b436d12f2e83389b504fc2d56285356820&type=&bd_page_type="
    body = body.format(account, password)
    conn = HTTPConnection("wappass.baidu.com", 80)
    conn.request("POST", "/passport/login", body, headers)
    resp = conn.getresponse()
    cookies += get_cookies_from_headers(resp.getheaders())
    save_cookies(headers, cookies)
    #print(gzip.decompress(resp.read()).decode())
    return True if resp.code == 302 else False

def get_user_info():
    headers.pop("Host")
    #headers["Host"] = "http://tieba.baidu.com"
    conn = HTTPConnection("tieba.baidu.com", 80)
    conn.request("GET", "/f/user/json_userinfo", "", headers)
    resp = conn.getresponse()
    data = gzip.decompress(resp.read()).decode("GBK")
    global userinfo
    userinfo = json.loads(data)

if __name__ == "__main__":
    account = input("请输入账号:")
    password = input("请输入密码:")
    ok = login(account, password)
    if ok:
        get_user_info()
        print(userinfo["data"]["user_name_weak"] + "~~~登陆成功", end="\n------\n")

