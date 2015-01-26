__author__ = 'Excelle'

import threading
balance = 0
lock = threading.Lock()


def change_it(n):
    global balance
    balance += n
    balance -= n


def run_thread(n):
    global lock
    for x in range(10000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()

t1 = threading.Thread(target=run_thread, args=(10, ))
t2 = threading.Thread(target=run_thread, args=(15, ))
t1.start()
t2.start()
t1.join()
t2.join()
print "Balance is %s" % balance