import multiprocessing
import time

class Test(multiprocessing.Process):
    
    def __init__(self, period, queue):
        super(Test, self).__init__()
        self.queue = queue
        self.period = period
        
    def run(self):
        while True:
            start = time.time()
            current = start
            
            while (current - start < self.period):
                current = time.time()
                
            print "Getting data"
            print self.queue.get()
