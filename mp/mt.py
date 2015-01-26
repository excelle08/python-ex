from multiprocessing import Pool

import os, time, random


def long_time_task(name):
    print "Run task: %s (%s)" % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print "Task %s runs %0.2f seconds" % (os.getpid(), (end - start))

if __name__ == '__main__':
    print 'Parent process: %s' % os.getpid()
    p = Pool()
    for i in range(11, 19):
        p.apply_async(long_time_task, args=(i, ))
    print 'Waiting for all processes...'
    p.close()
    p.join()
    print 'All processes are done.'