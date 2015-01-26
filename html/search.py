__author__ = 'Excelle'
from HTMLParser import HTMLParser
# from htmlentitydefs import name2codepoint
import urllib2


class MyHTMLParser(HTMLParser):
    current_tag = ""
    current_attr = []

    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False

    def handle_starttag(self, tag, attrs):
        if tag == "a" and self.lasttag == "h3":
            self.current_tag = "h3"
            self.current_attr = [('class', 'event-title')]
        else:
            self.current_tag = tag
            self.current_attr = attrs
        pass

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        try:
            for key, value in self.current_attr:
                if self.current_tag == "h3" and key == "class" and value == "event-title":
                    print "Title: %s" % data
                elif self.current_tag == "time" and key == "datetime":
                    print "Date : %s" % data
                elif self.current_tag == "span" and key == "class" and value == "event-location":
                    print "At   : %s" % data
                else:
                    pass
        except KeyError:
            pass
        except TypeError:
            print self.current_attr

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

url = "http://www.python.org/events/python-events/"
f = urllib2.urlopen(url)
data = f.read()

parser = MyHTMLParser()
parser.feed(data)