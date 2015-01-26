__author__ = 'Excelle'

import socket

s = socket.socket()
s.connect(("127.0.0.1", 9999))
print s.recv(1024)

while True:
    data = raw_input(">> ")
    s.send(data)
    print(s.recv(1024))
    if data == "exit":
        break
s.close()