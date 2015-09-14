# Echo server program
import socket
import numpy as np
import json
import cPickle

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50009              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

n = np.array([1.2, 2.4, 3.6])

conn.sendall(str(3) + ']')

for i in range(5):
    print str(n)
    conn.sendall(str(n))
    
conn.close()
