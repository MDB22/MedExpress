import multiprocessing
import time
from log import *

class WorldStateUpdater(multiprocessing.Process):
    def __init__(self, world_state, log_q):
        super(WorldStateUpdater, self).__init__()
        self.log_q = log_q

    def run(self):
        while True:
            pass

class WorldState():
    def __init__(self):
        pass