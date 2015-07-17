import multiprocessing
import time
from logging import log

class WorldStateUpdater(multiprocessing.Process):
    def __init__(self, world_state, log_q):
        super(WorldStateUpdater, self).__init__()
        self.world_state = world_state
        self.log_q = log_q

    def run(self):
        while True:
            self.world_state.setTest(self.world_state.getTest() + "1")
            time.sleep(3)

class WorldState():
    def __init__(self):
        self.test = "test world state"

    #TODO set up attibutes / properties
    def getTest(self):
        return self.test
    #TODO Locking on writes
    def setTest(self, test):
        self.test = test