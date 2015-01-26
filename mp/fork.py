__author__ = 'Excelle'

import os


print "Process %s starts." % os.getpid()

pid = os.fork()
if pid == 0:
    print "This is the child process: %s and the parent process is (%s)" % (os.getpid(), os.getppid())
else:
    print "PAR: %s created a child process: %s" % (os.getpid(), pid)
