import multiprocessing
from log import *

class Flight(multiprocessing.Process):
    def __init__(self, uav_state, world_state, flight_command_p, vehicle_command_p, log_q):
        pass

    def run(self):
        while True:
            pass