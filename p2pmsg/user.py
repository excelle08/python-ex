__author__ = 'Excelle'

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib2
import socket
import config
import hashlib
import re

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(16))
    password = Column(String(32))
    wan_ip = Column(String(16))
    lan_ip = Column(String(16))
    nickname = Column(String(20))


def get_lan_ip():
    return socket.gethostbyname(socket.gethostname())


def get_wan_ip():
    opener = urllib2.urlopen(config.ip_get_url)
    data = opener.read()
    return re.search(r'\d+\.\d+\.\d+\.\d+', data).group(0)


def initConnection():
    engine = create_engine('mysql+mysqlconnector://%s:%s@%s:3306/%s' %
                           (config.db_user, config.db_password, config.db_host, config.db_name))
    DBSession = sessionmaker(bind=engine)
    return DBSession


def reg_user(DBSession, username, password, nickname):
    session = DBSession()
    u = User()
    u.username = username
    u.password = hashlib.md5(password).hexdigest()
    u.nickname = nickname
    u.wan_ip = get_wan_ip()
    u.lan_ip = get_lan_ip()
    session.add(u)
    session.commit()
    session.close()


def query_user(DBSession, username):
    session = DBSession()
    user = session.query(User).filter(User.username == username).one()
    session.close()
    return user


def login_user(DBSession, username, password):
    pwd_hash = hashlib.md5(password).hexdigest()
    session = DBSession()
    user = session.query(User).filter(User.username == username).filter(User.password == pwd_hash).one()
    session.close()
    return user


def remove_user(DBSession, username):
    session = DBSession()
    u = query_user(DBSession, username)
    session.delete(u)
    session.commit()
    session.close()


def user2dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'wan_ip': user.wan_ip,
        'lan_ip': user.lan_ip,
        'nickname': user.nickname
    }