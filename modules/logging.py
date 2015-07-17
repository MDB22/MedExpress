import multiprocessing
import time
from log import *

class Logging(multiprocessing.Process):
    def __init__(self, log_q):
        super(Logging, self).__init__()
        self.log_q = log_q

    def run(self):
        while True:
            log = self.log_q.get()
            print log