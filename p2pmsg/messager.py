__author__ = 'Excelle'
'''
    Messager main program
'''

import socket
import json
import re
import threading
import pickle
import time
import datetime
import cfg
import user

user_list = []


def retrieve_user_list(encoded_str):
    global user_list
    lst = pickle.load(encoded_str)
    for i in lst:
        user_list.append(json.load(i, object_hook=user.dict2user))


def thread_login(sock, addr):
    global username, password, user_list
    sock.connect(addr)
    first_str = sock.recv(1024)
    if first_str == '200 Accepted':
        while True:
            sock.send('login\r\n' + username + ';' + password)
            packet = sock.recv(4096)
            header, data = re.split("\r\n", packet, 1)
            if header == '201 OK':
                user_list = []
                retrieve_user_list(data)
            else:
                print(header + ': FAILED TO LOGIN.')
                exit()
            time.sleep(30)
    else:
        print("Error connecting to server.")
        exit()


def thread_register(sock, addr, name, pwd, nk):
    sock.connect(addr)
    first_str = sock.recv(1024)
    if first_str == '200 Accepted':
        sock.send('register\r\n' + name + ';' + pwd + ';' + nk)
        result = sock.recv(1024)
        head, data = re.split('\r\n', result, 1)
        if head == '201 OK':
            print("Registration successful.")
            exit()
        else:
            print("Error occured: " + head)
            print(data)
            exit()
'''
    Message format:
        <Nickname>\r\n
        <Timestamp>\r\n
        <Body>
'''


def thread_receiver(sock, addr):
    sock.connect(addr)
    while True:
        raw_data = sock.recv(4096)
        name, timestamp, message = re.split('\r\n', raw_data, 2)
        print(name + " / " + timestamp)
        print(message)
        # sock.send('202 GET')
    pass


def thread_sender(sock, addr, nickname):
    sock.connect(addr)
    while True:
        text = raw_input(">>>")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        sock.send(nickname + '\r\n' + now + '\r\n' + text)


def register():
    usr = raw_input("Username:")
    pwd = raw_input("Password:")
    nkname = raw_input("Nickname:")
    return usr, pwd, nkname

# Step 1. Establish connection with central server
s_svr = socket.socket()
t_svr_login = threading.Thread(target=thread_login, args=(s_svr, (cfg.server_ip, cfg.server_port)))

opt = raw_input("Login(L) or Register(R)?")
if opt == 'R':
    u, p, n = register()
    t_reg = threading.Thread(target=thread_register, args=(s_svr, (cfg.server_ip, cfg.server_port), u, p, n))
    t_reg.start()
    t_reg.join()

else:
    username = raw_input("Username:")
    password = raw_input("Password:")
    t_svr_login.start()
    print("Logging in....")
    time.sleep(5)
    for usr in user_list:
        ts = threading.Thread(target=thread_sender, args=(s_svr, (usr.lan_ip, cfg.port), usr.nickname))
        tr = threading.Thread(target=thread_receiver, args=(s_svr, (usr.lan_ip, cfg.port), usr.nickname))
        ts.start()
        tr.start()