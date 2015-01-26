__author__ = 'Excelle'

from multiprocessing.managers import BaseManager
import random, time, Queue


task_queue = Queue.Queue()
result_queue = Queue.Queue()


class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)

manager = QueueManager(address=('127.0.0.1', 5000), authkey='abc')
manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()

for i in range(20):
    n = random.randint(0, 10000)
    print('Put task %d....' % n)
    task.put(n)

print 'Trying to get results..'

while True:
    try:
        r = result.get(timeout=10)
        print 'Result: %s' % r
    except BaseException:w
        print 'All results received..Aborting...'
        break

manager.shutdown()