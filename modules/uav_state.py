import multiprocessing
import time
from log import *

class UavStateUpdater(multiprocessing.Process):
    def __init__(self, uav_state, vehicle, log_q):
        super(UavStateUpdater, self).__init__()
        self.log_q = log_q

    def run(self):
        while True:
            pass

class UavState():
    def __init__(self):
        pass