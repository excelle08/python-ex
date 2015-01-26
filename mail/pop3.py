# -*- coding: utf-8 -*-
__author__ = 'Excelle'

import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                # DEcode
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % (' ' * indent, header, value))
    if msg.is_multipart():
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%sPart %s' % (' ' * indent, n))
            print('%s------------------' % ' ' * indent)
            print_info(part, indent+1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            # 不是文本,作为附件处理:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

# Basic information
email = "suwei779@126.com"
password = "Experience7.9"
pop3_server = "pop3.126.com"

# Connect to POP3 server
server = poplib.POP3(pop3_server)
# This is to DISPLAY or HIDE debug info
server.set_debuglevel(1)
# This is to display welcome message from the server.
print server.getwelcome()
# Authentication
server.user(email)
server.pass_(password)
# Get messages numbers and size.
print("Messages: %s, Size: %s" % server.stat())
# Method list() returns all email IDs
resp, mails, octets = server.list()
print mails
# Get the latest mail
index = len(mails)
resp, lines, octets = server.retr(index)
# Variable lines stores every line of the original mail content.
# This is to retrieve the whole text of the mail.
content = '\r\n'.join(lines)
# Parse the mail
msg = Parser().parsestr(content)
print_info(msg)
# This is to delete the mail of index X on the server
# server.dele(X)
# Close connection
server.quit()
