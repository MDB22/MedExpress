import multiprocessing
import time
from uav_logging import *

class UavStateUpdater(multiprocessing.Process):
    def __init__(self, uav_state, vehicle_command, log_q):
        super(UavStateUpdater, self).__init__()
        self.uav_state = uav_state
        self.vc_send, self.vc_recv, self.vc_send_lock, self.vc_recv_lock = vehicle_command
        self.log_q = log_q
        self.module_name = self.__class__.__name__

    def run(self):
        while True:
            #self.uav_state.setTest(self.uav_state.getTest() + "1")
            time.sleep(3)

class UavState():
    def __init__(self):
        self.test = "test uav state"
        self.module_name = self.__class__.__name__

    #TODO set up attibutes / properties
    def getTest(self):
        return self.test
    #TODO Locking on writes
    def setTest(self, test):
        self.test = test