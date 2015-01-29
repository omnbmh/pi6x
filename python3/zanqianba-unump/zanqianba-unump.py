#/usr/bin/python

import os
import ConfigParser
# read idx 
config = ConfigParser.ConfigParser()
config.readfp(open("unump.ini"))

idx = config.getint("global","idx");
print(idx);

for line in open("unump.txt"):
    #print(str(idx) + line)
    line = line.strip('\r\n')
    command = "java -jar unump.jar zqb_00000000" + str(idx) +" " + line;
    print(command);
    os.system(command)
    idx = idx + 1

config.set("global","idx",idx);
config.write(open("unump.ini","w"))
