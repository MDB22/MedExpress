import multiprocessing
import time
from logging import Log

class UavStateUpdater(multiprocessing.Process):
    def __init__(self, uav_state, vehicle, log_q):
        super(UavStateUpdater, self).__init__()
        self.uav_state = uav_state
        self.log_q = log_q

    def run(self):
        while True:
            self.uav_state.setTest(self.uav_state.getTest() + "1")
            time.sleep(3)

class UavState():
    def __init__(self):
        self.test = "test uav state"

    #TODO set up attibutes / properties
    def getTest(self):
        return self.test
    #TODO Locking on writes
    def setTest(self, test):
        self.test = test