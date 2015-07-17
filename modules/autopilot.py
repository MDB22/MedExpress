import multiprocessing
import time
from log import *

class Autopilot(multiprocessing.Process):
    def __init__(self, vehicle, vehicle_command, log_q):
        super(Autopilot, self).__init__()
        self.log_q = log_q

    def run(self):
        while True:
            pass