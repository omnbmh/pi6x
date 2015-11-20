#!/bin/python
# -*- coding:utf-8 -*-

import threading, time, httplib
import urllib
import random

DES_KEY='1A70A1DD249952FE16DDE84FEF1B5B4A'

HOST='192.168.86.1'
PORT=8080
DECRYPT_URI="/demome-api-0.1/api/security/des/decrypt"
ENCRYPT_URI="/demome-api-0.1/api/security/des/encrypt"
BODY='{"prodType":"3","systemIdentify":"0"}'
BODY='cuXuIrcm5I479uH0fp8SjN7stmdXBh6SUwDYI8e5fIXdr9hptIbYwA=='
BODY='{"prodNo":"20151022143238757453","prodType":"3","systemIdentify":"0","investorNo":"100058796357"}'
BODY='eRl9vRLqNNdMXGXOg5uKJnFrKlKeswwgUcmwoDrFeddMJFe7sENHXTv24fR+nxKM3uy2Z1cGHpJTANgjx7l8hUmqmrh0y71Bzvb490/c0F62F59QM/elehaDs3wqZOITLVrpyakm4c0='
#BODY='5EIbC6fLuksbUwEOJLg0ihCUSDS+dAZK21ftqiXs++MJXf9nhutP7A=='

class RequestThread(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.test_count = 0
        self.name = thread_name
        
    def run(self):
        self.test_performace()
        
    def test_performace(self):
        try:
            st = time.time
            params = urllib.urlencode({'body': BODY})
            headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
            conn = httplib.HTTPConnection(HOST,PORT,False,100)
            conn.request('POST',URI,params,headers)
            res = conn.getresponse()
            print self.name + str(res.status)
            print res.reason
            print res.read()
        except Exception,e:
            print e
            
            
thread_count = 0

i = 0
while i<thread_count:
    #print "thread" + str(i) + "start..."
    t = RequestThread("thread" + str(i))
    t.start()
    i += 1
    
    
def create_query_product_body():
    list_enctypt_text = []
    list_text = []
    times = 100
    i = 0
    while i < times:
        i=i+1
        #read user id from file
        for line in open("userid.txt"):
            json_body = "{'systemIdentify':'1','investAmount':'%d',prodNo:'%s','investorNo':'%s'}"
            prodNo = '20151021183819324146'
            userId = line.strip('\r\n')
            print userId
            json_body = json_body % (random.randint(100, 500),prodNo,userId)
            print json_body
            params = urllib.urlencode({'key': DES_KEY,'text':json_body})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            conn = httplib.HTTPConnection(HOST,PORT,False,100)
            conn.request('POST',ENCRYPT_URI,params,headers)
            res = conn.getresponse()
            #print res.status
            #print res.reason
            res_text = res.read()
            res_text = res_text.replace('\n','').replace('\r','')
            print res_text
            list_text.append(json_body+'\n')
            list_enctypt_text.append(res_text+'\n')
        
    file_object = open('createInvestInfo.txt', 'w')
    file_object.writelines(list_text)
    file_object.close()
    file_object = open('createInvestInfo_encrypt.txt', 'w')
    file_object.writelines(list_enctypt_text)
    file_object.close()
        
create_query_product_body()