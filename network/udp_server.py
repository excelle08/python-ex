__author__ = 'Excelle'

import socket
import hashlib
import threading


def do_connection(data, addr, sock):
    print("Data from %s:%s" % addr)
    print data
    sock.sendto(str(hashlib.md5(data).hexdigest()), addr)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))

print 'UDP Server binded on port 9999..'
while True:
    data, addr = s.recvfrom(1024)
    t = threading.Thread(target=do_connection, args=(data, addr, s))
    t.start()

