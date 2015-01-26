# -*- coding: utf-8 -*-
__author__ = 'Excelle'

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

# Basic information
from_addr = 'suwei779@126.com'
password = 'Experience7.9'
to_addr = '838731891@qq.com'
smtp_svr = 'smtp.126.com'
# Build header
msg = MIMEMultipart('alternative')
msg['From'] = format_addr(u'金坷垃三人组 <%s>' % from_addr)
msg['To'] = format_addr(u'元首 <%s>' % to_addr)
msg['Subject'] = Header(u'Python大法好', 'utf-8').encode()
# Add attachments
with open('./at.c', 'rb') as f:
    # Configure MIME and filename:
    mime = MIMEBase('text', 'plain', filename='./at.c')
    mime.add_header('Content-Disposition', 'attachment', filename='./at.c')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # Load content
    mime.set_payload(f.read())
    # Base64 Encode
    encoders.encode_base64(mime)
    # Add to MSG
    msg.attach(mime)
with open('./attachment.jpg', 'rb') as f:
    # Configure MIME and filename:
    mime = MIMEBase('image', 'jpeg', filename='./attachment.jpeg')
    mime.add_header('Content-Disposition', 'attachment', filename='./attachment.jpeg')
    mime.add_header('Content-ID', '<1>')
    mime.add_header('X-Attachment-Id', '1')
    # Load content
    mime.set_payload(f.read())
    # Base64 Encode
    encoders.encode_base64(mime)
    # Add to MSG
    msg.attach(mime)
# Add HTML
s = ""
with open('./content.html', 'r') as r:
    s = r.read()
msg.attach(MIMEText(s, 'html', 'utf-8'))

# Send the email
server = smtplib.SMTP(smtp_svr, 25)
server.set_debuglevel(0)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
