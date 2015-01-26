__author__ = 'Excelle'

# Central Server for user management
# Register, Login, Query, Removal
'''
    1. Connection
        a.Client connects to this server
        b.Server returns "200 Accepted" to certify.
    2. Command
        a.Client sends a command.
        b.Server responses.
    3. Register
        a.CMD='register'
        b.Following data: <USERNAME>;<PASSWORD>;<NICKNAME>
        c."201 OK" for finish and "500 FAIL" for failure.
        d.If fails, returns error message.
    4. Log in
        a.CMD='login'
        b.Data=user;password
        c.Server verifies
        d."201 OK" for success and "403 WRONG" for failure
    5. Log out
        a.CMD='logout'
        b.Data=user;password
        c.Verification
    6. Use '\r\n' to split command and data
'''

import socket
import threading
import user
import re
import json

current_ip = user.get_wan_ip()
current_port = 12345
user_lists = []


def resp(sock, addr):
    print "Accepted TCP connection from %s:%s" % addr
    sock.send("200 Accepted")
    while True:
        data = sock.recv(1024)
        cmd, content = re.split('\r\n', data)
        if cmd == 'register':
            inf = re.split(';', content)
            try:
                user.reg_user(db_session, inf[0], inf[1], inf[2])
                sock.send("201 OK\r\n")
            except BaseException, e:
                sock.send("500 FAIL\r\n")
                sock.send(e.message)
        elif cmd == 'login':
            inf = re.split(';', content)
            try:
                u = user.login_user(db_session, inf[0], inf[1])
                if u:
                    user_lists.append(u)
                    sock.send("201 OK\r\n")
                    
                else:
                    sock.send("403 WRONG\r\n")
            except BaseException, e:
                sock.send("500 FAIL:\r\n")
                sock.send(e.message)
        elif cmd == 'logout':
            inf = re.split(';', content)
            try:
                u = user.login_user(db_session, inf[0], inf[1])
                if u:
                    for i in xrange(0, len(user_lists)-1):
                        if user_lists[i].username == u.username and user_lists[i].password == u.password:
                            user_lists.pop(i)
                            sock.send("201 OK\r\n")
                            sock.send("Bye")
                            print("Connection with %s:%s has been closed." % addr)
                            break
                        else:
                            sock.send("403 WRONG\r\n")
            except BaseException, e:
                sock.send("500 FAIL:\r\n")
                sock.send(e.message)
        else:
            pass



s = socket.socket()
s.bind((current_ip, current_port))
s.listen(16)

db_session = user.initConnection()

while True:
    sock, addr = s.accept()
    t = threading.Thread(target=resp, args=(sock, addr))
    t.start()