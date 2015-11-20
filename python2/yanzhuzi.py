#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'c8d8z8@gmail.com'

import json
import commonlib.http
from bs4 import BeautifulSoup
import re
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')

import sqlite3
conn = sqlite3.connect('gyq.db3')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS yanzhuzi (fname varchar(100),name varchar(100),lv varchar(100),imgs_url varchar(5000),report_url varchar(1000))')
cur.execute('delete from yanzhuzi')
print_encode='gbk'

#网站基础地址
web_url='http://www.fact-eye.com:9000/ho/'
#医院编码
hospitalid=''
#账号
acc_user=''
#密码
acc_pwd=''
#病变级别
illness_level=''
#图片质量
img_quality=''
#筛查区分
screen_type=''
#时间 使用','分割
date_section='0'

import ConfigParser

ini_file = ConfigParser.ConfigParser()
ini_file.read('yanzhuzi.ini')

web_url = ini_file.get('global','web_url')
hospitalid = ini_file.get('global','hospitalid')
acc_user = ini_file.get('global','acc_user')
acc_pwd = ini_file.get('global','acc_pwd')

illness_level = ini_file.get('search_parameter','illness_level')
img_quality = ini_file.get('search_parameter','img_quality')
screen_type = ini_file.get('search_parameter','screen_type')
date_section = ini_file.get('search_parameter','date_section')

print (web_url,hospitalid,acc_user,acc_pwd,illness_level,img_quality,screen_type,date_section)


def login():
    url = web_url+'ho_login.htm?ajaxSession=E8A6CBFE4F43E3A4A52B5A45853AE82A'
    data = 'flg=1&userid='+acc_user+'&userpw='+acc_pwd+'&hospitalid='+hospitalid+'&cpu='
    data = commonlib.http.request(url,commonlib.http.paramparse(data))
    data=json.loads(data)
    #print data
    if len(data) > 0:
        print u'登陆成功!'.encode(print_encode)
    else:
        print u'登陆失败!'.encode(print_encode)

def get_list(page):
    url = web_url+'diabetic_retinopathy_manager_ajax.htm?ajaxSession=92935BC2719258032A2134E503047216'
    data = 'flg=1&'
    data += 'page='+str(page)+'&'
    data += 'moreSearchFlg=1&'
    data += 'searchHospitalId='+hospitalid+'&'
    data += 'searchPatientName=&'
    data += 'searchPatientSex=&'
    data += 'searchPatientAge=&'
    if date_section == '0':
        data += 'dateFlg=0&'
        data += 'searchUploadDateF=&'
        data += 'searchUploadDateT=&'
    else:
        date_arr = date_section.split(',')
        data += 'dateFlg='+date_arr[0]+'&'
        data += 'searchUploadDateF='+date_arr[1]+'&'
        data += 'searchUploadDateT='+date_arr[2]+'&'
    data += 'searchDRno=&'
    data += 'searchDiseaseFlg='+screen_type+'&'
    data += 'searchStatus=&'
    data += 'searchRemarks=&'
    data += 'searchDiabeteGrade='+illness_level+'&'
    data += 'searchImageQuality='+img_quality+'&'
    data += 'searchBloodCountF=&'
    data += 'searchBloodCountT=&'
    data += 'searchBloodAllAreaF=&'
    data += 'searchBloodAllAreaT=&'
    data += 'searchTwUnit=1'

    data = commonlib.http.request(url,commonlib.http.paramparse(data))
    #print data
    data=json.loads(data)
    print (u'获取第'+str(page)+u'页列表成功!').encode(print_encode)
    if len(data) > 0:
        if data[0][u'result'] == u'true':
            list_data = data[0][u'list']
            print (u'获取第'+str(page)+u'页列表数据成功').encode(print_encode)
            #print list_data
            
            #查找数据列
            soup = BeautifulSoup(list_data)
            rows = soup.find_all(name='tr')
            if len(rows) <= 0:
                print u'获取列表数据完成'.encode(print_encode)
                return False
            for row in rows:
                # 解析数据 获取有价值的数据

                # 区分
                tname = row.contents[5].string
                #print tname
                # 姓名
                name = row.contents[1].label.string
                #print name
                # 分级 
                lv = row.contents[6].string
                #print lv
                # 获取图片地址
                imgs_str = None
                btn = row.find(href=re.compile('diabetes_eyes_edit_image.htm'))
                if btn != None:
                    url = web_url + btn.attrs[u'href']
                    print url
                    data = commonlib.http.request(url)
                    soup_imgs = BeautifulSoup(data)
                    imgs = soup_imgs.find_all(attrs={'name':re.compile('img_[od]$')})
                    #imgs = soup_imgs.find_all('img')
                    #print imgs
                    if len(imgs) > 0:
                        imgs_str = ''
                    for img in imgs:
                        #print img
                        img_str = web_url + img.attrs[u'src']
                        #print img_str
                        imgs_str += img_str+','
                        #print imgs_str
                    if imgs_str != None:
                        imgs_str = imgs_str.strip(',')
                #print imgs_str
                #查看报告地址
                report_url = None
                btn = row.find(href=re.compile('diabetes_eyes_result_image.htm'))
                if btn != None:
                    report_url = web_url + btn.attrs[u'href']
                t = (tname,name,lv,imgs_str,report_url)
                print t
                # write in db3
                cur.execute('insert into yanzhuzi values (?,?,?,?,?)',t)
                
                #break
            
        else:
            print u'获取列表数据失败'.encode(print_encode)
    else:
        print u'获取列表失败!'.encode(print_encode)
    return True
    
def download_file():
    cur.execute('select *from yanzhuzi')
    rows = cur.fetchall()
    for row in rows:
        print row
        fpath = hospitalid+'-RESULTS/'+row[0]+'/'+row[1]+'-'+row[2]+'/'
        if row[3] != None:
            img_arr = row[3].split(',')
        else:
            img_arr = []
        i = 0
        for img in img_arr:
            fname = str(i)+'-more.jpg'
            if i == 0:
                fname = '右原.jpg'
                img2 = img.replace('fundus','fundus2')
                img3 = img.replace('fundus','fundus3')
                commonlib.http.download(img,fpath.encode('gbk'),'右深1.jpg'.encode('gbk'))
                commonlib.http.download(img,fpath.encode('gbk'),'右深2.jpg'.encode('gbk'))
            if i == 1:
                fname = '右规.jpg'
            if i == 2:
                fname = '左原.jpg'
                img2 = img.replace('fundus','fundus2')
                img3 = img.replace('fundus','fundus3')
                commonlib.http.download(img,fpath.encode('gbk'),'左深1.jpg'.encode('gbk'))
                commonlib.http.download(img,fpath.encode('gbk'),'左深2.jpg'.encode('gbk'))
            if i == 3:
                fname = '左原.jpg'
            commonlib.http.download(img,fpath.encode('gbk'),fname.encode('gbk'))
            i+=1

def run():
    login()
    
    page = 1
    isOk = True
    while isOk:
        isOk = get_list(page)
        page+=1
    conn.commit()
    download_file()
    
run()
conn.close()