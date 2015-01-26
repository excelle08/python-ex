__author__ = 'Excelle'

import socket

# Establish TCP connection
s = socket.socket()
s.connect(('www.baidu.com', 80))
s.send('GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n')

# Retrieve data
buffer = []
while True:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = ''.join(buffer)
# Close connection
s.close()
# Process HTTP returns
header, body = data.split('\r\n\r\n', 1)
print header
# Write HTML body to file
with open("index.html", "wb") as f:
    f.write(body)
