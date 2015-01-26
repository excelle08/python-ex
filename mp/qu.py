__author__ = 'Excelle'

from multiprocessing import Queue
from multiprocessing import Process
import os, time, random


# Write data to queue
def write(q):
    for value in ['A', 'B', 'C']:
        print 'Put %s into the queue..' % value
        q.put(value)
        time.sleep(random.random())


def read(q):
    while True:
        value = q.get(True)
        print 'Get %s from the queue.' % value


if __name__ == '__main__':
    q = Queue()
    proc_write = Process(target=write, args=(q, ))
    proc_read = Process(target=read, args=(q, ))
    proc_write.start()
    proc_read.start()
    proc_write.join()
    proc_read.terminate()