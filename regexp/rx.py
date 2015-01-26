__author__ = 'Excelle'

import re


date_str = raw_input("Please enter a date(MM-DD):")
time_str = raw_input("Please enter a time(HH:MM:SS)")

mt = re.match(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:'
              r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:'
              r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])$', time_str)

md = re.match(r'^(0[1-9]|1[0-2]|[0-9])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]|[0-9])$', date_str)

try:
    print mt.groups()
    print md.groups()
except AttributeError, ex:
    print 'Failed to match: ' + ex.message

