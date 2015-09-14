import multiprocessing
import time

from cPickle import loads

class Test(multiprocessing.Process):

    def __init__(self, period, queue):
        super(Test, self).__init__()

        self.period = period
        
        self.queue = queue

    def run(self):
        start = time.time()
        current = start

        while True:
            current = time.time()
            
            if (current - start > self.period):
                start = time.time()
                data = loads(self.queue.get())
                print 'Receiving from Queue', len(data), data[0]
