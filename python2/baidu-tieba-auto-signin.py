#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'c8d8z8@gmail.com'

'''
    百度贴吧自动签到
'''
import commonlib.baidu

tieba = commonlib.baidu.BaiduTieba()

def start():
    if tieba.is_login():
        tieba.sign()
    else:
        acc = raw_input('请输入账号:')
        pwd = raw_input('请输入密码:')
        tieba.login(acc,pwd)
        start()
    
start()