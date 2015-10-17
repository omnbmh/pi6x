#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'c8d8z8@gmail.com'

of = 'dnsmasq.conf.hosts'

# 读取hosts文件
infile = open('hosts.2015-10-17.txt','r')

# 写入dnsmasq配置文件
outfile = open(of,'w')

ft = ''
for ipline in infile:
    if(ipline.startswith('#') == False):
        ipline = ipline.replace('\t',' ')
        arr = ipline.split(' ')
        #print arr
        l = len(arr)
        if l>1 and arr[1].strip() != '':
            dnsstr = 'address=/' +arr[1].strip('\n')+'/'+arr[0]+'\n'
            print dnsstr
            ft = ft + dnsstr
infile.close()
outfile.write(ft)
outfile.close()




