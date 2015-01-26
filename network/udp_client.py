__author__ = 'Excelle'

import socket

s = socket.socket(type=socket.SOCK_DGRAM)
while True:
    data = raw_input(">>")
    s.sendto(data, ('127.0.0.1', 9999))
    print s.recv(1024)
    if data == "exit":
        break

s.close()