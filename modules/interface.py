import multiprocessing
import time
from uav_logging import *

class BaseCommunications(multiprocessing.Process):
    def __init__(self, flight_command, log_q, ilog_q):
        super(Interface, self).__init__()
        self.fc_send, self.fc_recv, self.fc_lock = flight_command
        self.log_q = log_q
        self.ilog_q = ilog_q
        self.module_name = self.__class__.__name__

    def run(self):
        while True:
            #print self.ilog_q.get()
            # self.log_q.put("test interface")
            # with self.fc_send_lock:
            #     self.fc_send.send("interface flight com")
            # with self.fc_recv_lock:
            #     print self.fc_recv.recv()
            # time.sleep(2)
            pass
