import multiprocessing
import time

class Logging(multiprocessing.Process):
    def __init__(self, log_q):
        super(Logging, self).__init__()
        self.log_q = log_q

    def run(self):
        while True:
            print self.log_q.get()

class Log:
    """ Data structure for logs

    module: Name of logged module
    data:   Dictionary of logged attributes
    """
    def __init__(self, module, data):
        pass

    def __str__(self):
        print "TODO"