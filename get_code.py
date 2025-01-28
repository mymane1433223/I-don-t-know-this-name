from socket import *
import sys
name=sys.argv[1]
if len(sys.argv)>2:
    path=sys.argv[2]
else:
    path=r'/data/data/com.termux/files/'
s=socket()
s.connect(('47.94.245.67',6999))
s.send('g'.encode())
s.send(name.encode())
code=s.recv(102400).decode()
with open(path+name,'w') as f:
    f.write(code)
s.close()