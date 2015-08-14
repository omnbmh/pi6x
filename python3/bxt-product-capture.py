#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- author: c8d8z8@gmail.com

import httputils;
from bs4 import BeautifulSoup
import sqlite3

# setting sqlite3
conn = sqlite3.connect('bxt.db3')
cur = conn.cursor()

URL="http://bxt.itoumi.com/invest/list.html?minProdAmount=&maxProdAmount=&minDueDate=&maxDueDate=&orderParam=&numPerPage=10&prePage=1&orderField=YEAR_IRR&orderDirection=ASC&nextPage=2&ttPage=283&pageNum="

def captrue():
    cur_page = 1
    while(cur_page<=250):
        print('正在抓取第'+str(cur_page)+'页')
        data = httputils.request(URL+str(cur_page),{})
        #print(data)
        soup = BeautifulSoup(data)
        #print(soup.prettify().encode('utf-8'))
        #soup.prettify()
        print(soup.title)
        rows = soup.findAll('tr')
        for row in rows:
            deal_rows(row)
        cur_page+=1
    conn.commit()
    conn.close()
        
        
def deal_rows(row):
    #print(row.attrs)
    #print('class' in row.attrs)
    if('class' in row.attrs and (row.attrs['class'][0] == 'row1' or row.attrs['class'][0] == 'row0')):
        cols = row.findAll('td')
        #print(type(row))
        #print(type(cols[0]))
        #产品名称
        if(cols[0].find('i') != None):
            name = ''.join(cols[0].find('a').get_text().split())
            isEnd = 1
        else:
            name = ''.join(cols[0].get_text())
            isEnd = 0
        #年化收益
        yearRate = ''.join(cols[1].get_text().split())
        #到期天数
        toEndDays = ''.join(cols[2].span.get_text().split())
        #成交笔数
        tradeNum = ''.join(cols[3].get_text().split())
        #产品总金额
        tradeAmount = ''.join(cols[4].get_text().split())
        #详情链接
        link = cols[6].a.attrs['href']
        #print(type(name))
        #print(type(str(isEnd)))
        #print(type(yearRate))
        #print(type(toEndDays))
        #print(type(tradeNum))
        #print(type(tradeAmount))
        #print(type(link))
        t1 = (name.replace('变现贷',''),name,str(isEnd),yearRate,toEndDays,tradeNum,tradeAmount,link)
        t2 = (None,None,None)
        if(isEnd):
            t2 = dealDetail('https://bxt.itoumi.com/%s' % link)
            print('%s %s %s' % t2)
            
        print('%s %s %s %s %s %s %s' % (name,str(isEnd),yearRate,toEndDays,tradeNum,tradeAmount,link))
        print('-----------------------------------')
        cur.execute('insert into bxt_trade_apply values (?,?,?,?,?,?,?,?,?,?,?)',t1+t2)
        
def dealDetail(url):
    data = httputils.getData(url)
    soup = BeautifulSoup(data)
    toEndDate = ''.join(soup.find(attrs={'class':'hx_pro_info'}).findAll('p')[2].get_text().split())
    startBuyTime =''.join(soup.find(attrs={'class':'hx_shopover'}).findAll('span')[0].get_text().split())
    endBuyTime =''.join(soup.find(attrs={'class':'hx_shopover'}).findAll('span')[1].get_text().split())
    return (toEndDate,startBuyTime,endBuyTime)
captrue()