__author__ = 'Excelle'

from HTMLParser import HTMLParser
# from htmlentitydefs import name2codepoint
import urllib2


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('Start Tag: %s' % tag)
        print('Attributes:')
        for key, value in attrs:
            print "%s | %s" % (key, value)
        print("---------------------------")
    def handle_endtag(self, tag):
        # print('</%s>' % tag)
        pass

    def handle_startendtag(self, tag, attrs):
        print('Start-end tag: %s' % tag)
        print('Attributes:')
        for key, value in attrs:
            print("%s | %s" % (key,value))
        print("---------------------------")

    def handle_data(self, data):
        print('Data: %s' % data)
        print('LastTag: %s' % self.lasttag)

    def handle_comment(self, data):
        # print('<!-- -->')
        pass

    def handle_entityref(self, name):
        print('Entity Ref: %s;' % name)
        pass

    def handle_charref(self, name):
        print('Char Ref: %s;' % name)
        pass

url = "http://www.python.org/events/python-events/"
f = urllib2.urlopen(url)
data = f.read()

parser = MyHTMLParser()
parser.feed(data)