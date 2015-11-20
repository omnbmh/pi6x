#!/bin/python
# -*- coding:utf-8 -*-
# author c8d8z8@gmail.com

import sys
from Crypto.Cipher import DES
import base64
from Crypto import Random

def encrypt_des(key,text):
	iv = Random.get_random_bytes(8)
	des = DES.new(key,DES.MODE_CFB,iv)
	reminder = len(text)%8
	if reminder == 0:
		text+='\x08'*8
	else:
		text+=chr(8-reminder)*(8-reminder)
		
	return base64.encodestring(des.encrypt(text))
DES_KEY='DESCRYPT'
DES_KEY='1A70A1DD249952FE16DDE84FEF1B5B4A'

data = '{"prodType":"3","systemIdentify":"0"}'


print encrypt_des(DES_KEY,data)