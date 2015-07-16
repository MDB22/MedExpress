import multiprocessing
from log import *

class Interface(multiprocessing.Process):
    def __init__(self, flight_command_p, log_q):
        pass

    def run(self):
        while True:
            pass