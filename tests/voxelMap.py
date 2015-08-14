import multiprocessing
import time
from ..modules import lidarSystem

class Test(multiprocessing.Process):
    
    def __init__(self, period, queue):
        # Call superclass init
        super(Test, self).__init__()
        
        self.period = period
        self.queue = queue
        
    def run(self):
        
    	start = time.time()
    	current = start
    	
    	while True:
    	    current = time.time()
    	    
    	    if (current - start > period):
    	        print self.queue.get()

q = multiprocessing.Queue()

l = LidarSystem(5, q)
#t = Test(6, q)

l.start()
#t.start()