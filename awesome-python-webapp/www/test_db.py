__author__ = 'Excelle'

from model import User, Blog, Comment
from transwrap import db
from config import config


db.create_engine(config.mysql_username, config.mysql_password, config.mysql_database)

u = User(id='test', email='sb250@lanxiang.com', password='123456', image='about:blank', name='Wajueji')
u.insert()

print('New UID:'+u.id)
u1 = User.find_first('where email=?', 'sb250@lanxiang.com')
print 'find user\'s name:', u1.name

u1.delete()

u2 = User.find_first('where email=?', 'sb250@lanxiang.com')
print 'find user:', u2