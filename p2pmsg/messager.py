__author__ = 'Excelle'
'''
    Messager main program
'''

import socket
import json
import re
import threading
import pickle
import cfg
import user

user_list = []


def retrieve_user_list(encoded_str):
    lst = pickle.load(encoded_str)
    for i in lst:
        user_list.append(json.load(i, object_hook=user.dict2user))


def thread_login(sock, addr):
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
s_svr.connect((cfg.server_ip, cfg.server_port))
t_svr = threading.Thread(target=thread_login, args=(s_svr, (cfg.server_ip, cfg.server_port)))

opt = raw_input("Login(L) or Register(R)?")
if opt == 'L':
    register()
else:
    username = raw_input("Username:")
    password = raw_input("Password:")
