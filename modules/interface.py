import multiprocessing
import time
from logging import Log

class Interface(multiprocessing.Process):
    def __init__(self, flight_command, log_q):
        super(Interface, self).__init__()
        self.fc_send, self.fc_recv, self.fc_send_lock, self.fc_recv_lock = flight_command
        self.log_q = log_q

    def run(self):
        while True:
            self.log_q.put("test interface")
            with self.fc_send_lock:
                self.fc_send.send("interface flight com")
            with self.fc_recv_lock:
                print self.fc_recv.recv()
            time.sleep(2)