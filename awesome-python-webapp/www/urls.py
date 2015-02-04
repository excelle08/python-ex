# -*- coding: utf-8 -*-
__author__ = 'Excelle'

from transwrap.web import get, view, post, ctx, interceptor, SeeOther, NotFound
from model import User, Blog
from apis import api
from apis import APIError, APIPermissionError, APIResourceNotFoundError, APIValueError
import re

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')

@view('blogs.html')
@get('/')
def index():
    blogs = Blog.find_all()
    # 查找登陆用户:
    user = User.find_first('where email=?', 'admin@example.com')
    return dict(blogs=blogs, user=user)

@api
@get('/api/users')
def register_user():
    i = ctx.request.input(name='', password='', email='')
    name = i.name.strip()
    email = i.email.strip().lower()
    password = i.password
    if not name:
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_MD5.match(email):
        raise APIValueError('password')
    user = User.find_first('where email=?', email)
    if user:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    user = User(name=name, password=password, email=email, image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email).hexdigest())
    user.insert()
    return user


@view('register.html')
@get('/register')
def register():
    return dict()

