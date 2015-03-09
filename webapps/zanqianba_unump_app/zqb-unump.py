#/usr/bin/python

import os
import ConfigParser
# read idx 
config = ConfigParser.ConfigParser()
config.readfp(open("unump.ini"))

def batch(){
    for line in open("unump.txt"):
        phone = line.strip('\r\n')
        unump(phone);
}
#从unump.txt读取手机号 批量执行
#batch()

def unump(phone):
    idx = config.getint("global","idx");
    command = "java -jar unump.jar zqb_00000000" + str(idx) +" " + phone;
    print('Send Command: '+command);
    print(command);
    os.system(command)
    config.set("global","idx",idx + 1);
    config.write(open("unump.ini","w")) 
