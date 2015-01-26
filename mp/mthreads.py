__author__ = 'Excelle'

import time
import threading


def loop(x, y):
    print "Thread %s is running..." % threading.current_thread().name
    for n in range(x, y):
        print "Thread %s --- %s" % (threading.current_thread().name, n)
        time.sleep(1)
    print "Thread %s ended." % threading.current_thread().name

print "Thread %s starts..." % threading.current_thread().name
t = threading.Thread(target=loop, name="Loop", args=(1, 6, ))
u = threading.Thread(target=loop, name="Mppq", args=(25, 31, ))
t.start()
u.start()
t.join()
u.join()
print "Thread %s ended..." % threading.current_thread().name
