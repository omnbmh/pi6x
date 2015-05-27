import platform;

print ("Just for demo how to python development under windows;");
print ("Current python version info is %s"%(platform.python_version()));
print ("uname=",platform.uname());

import os
hha = os.system('ping 10.105.77.1')
print('-------------------------------------')
print(hha)