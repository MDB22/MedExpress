import multiprocessing
import time
from uav_logging import *

class Flight(multiprocessing.Process):
    def __init__(self, uav_state, world_state, flight_command, vehicle_command, log_q):
        super(Flight, self).__init__()
        self.uav_state = uav_state
        self.world_state = world_state
        self.fc_send, self.fc_recv, self.fc_send_lock, self.fc_recv_lock = flight_command
        self.log_q = log_q
        self.module_name = self.__class__.__name__

    def run(self):
        while True:
            # log = Log(LogType.error, self.module_name, time.localtime(), {'test_flight':'error'})
            # self.log_q.put(log)
            # log = Log(LogType.notice, self.module_name, time.localtime(), {'test_flight':'notice'})
            # self.log_q.put(log)
            # log = Log(LogType.debug, self.module_name, time.localtime(), {'test_flight':'debug'})
            # self.log_q.put(log)
            # log = Log(LogType.stat, self.module_name, time.localtime(), {'test_flight':'stat'})
            # self.log_q.put(log)
            # time.sleep(5)
            #self.log_q.put("test flight")
            # with self.fc_send_lock:
            #     self.fc_send.send("flight interface answer")
            # with self.fc_recv_lock:
            #     print self.fc_recv.recv()
            # print self.uav_state.getTest()
            # print self.world_state.getTest()
            # time.sleep(2)
            pass