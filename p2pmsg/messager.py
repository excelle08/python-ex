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
import cfg
import user

user_list = []


def retrieve_user_list(encoded_str):
    lst = pickle.load(encoded_str)
    for i in lst:
        user_list.append(json.load(i, object_hook=user.dict2user))


def thread_login(sock, addr):
    global username, password
    sock.connect(addr)
    first_str = sock.recv(1024)
    if first_str == '200 Accepted':
        sock.send('login\r\n' + username + ';' + password)
        data = sock.recv(4096)
        retrieve_user_list(data)
    else:
        print("Error connecting to server.")
        exit()
    pass


def thread_register(sock, addr, user):
    pass


def thread_receiver(sock, addr):
    pass


def thread_sender(sock, addr):
    pass


def register():
    usr = raw_input("Username:")
    pwd = raw_input("Password:")
    nkname = raw_input("Nickname:")
    return usr, pwd, nkname

# Step 1. Establish connection with central server
s_svr = socket.socket()
t_svr = threading.Thread(target=thread_login, args=(s_svr, (cfg.server_ip, cfg.server_port)))

opt = raw_input("Login(L) or Register(R)?")
if opt == 'L':
    register()
else:
    username = raw_input("Username:")
    password = raw_input("Password:")