# coding:utf-8

from mtools.pathtools import *
os.chdir(cur_file_dir(sys.path[0]))

import urllib.request
import json

def requestXinghuo(mobile):
    data = "mobile=" + mobile
    req = urllib.request.Request('http://xinghuo.yixin.com/checkmobile.shtml',data.encode('utf-8'))
    req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53')
    res = urllib.request.urlopen(req).read().decode('utf-8')
    #print(res)
    print(data)
    print(res)
    return res
    
def save(mobile):
    print("start save -- " + mobile)
    file = open('m.txt','a')
    file.write(mobile+'\n');
    file.close();
    print("end save -- " + mobile)
    
def search():
    for i in range(99999999):
        mobile = "130" + "0" * (8 - len(str(i))) + str(i)
        res = requestXinghuo(mobile)
        res = json.loads(res)
        if res["resCode"] == "0":
            save(mobile)
    
search()