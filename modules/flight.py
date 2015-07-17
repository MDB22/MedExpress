import multiprocessing
import time
from log import *

class Flight(multiprocessing.Process):
    def __init__(self, uav_state, world_state, flight_command, vehicle_command, log_q):
        super(Flight, self).__init__()
        self.fc_send, self.fc_recv, self.fc_send_lock, self.fc_recv_lock = flight_command
        self.log_q = log_q

    def run(self):
        while True:
            self.log_q.put("test flight")
            with self.fc_recv_lock:
                print self.fc_recv.recv()
            with self.fc_send_lock:
                self.fc_send.send("flight interface answer")
            time.sleep(1)