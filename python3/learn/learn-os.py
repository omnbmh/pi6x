import os
import sys
print(os.getcwd())
p = os.path.dirname(sys.argv[0])
print(p)
os.chdir(p)
print(os.getcwd())
#print(''.join(os.getcwd(),os.path.abspath('.')))