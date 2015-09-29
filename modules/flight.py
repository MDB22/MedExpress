import multiprocessing
from time import sleep
from uav_logging import *

class Flight(multiprocessing.Process):
    def __init__(self, uav_state, world_state, flight_command, vehicle_command, log_q):
        super(Flight, self).__init__()
        self.uav_state = uav_state
        self.world_state = world_state
        self.fc_send, self.fc_recv, self.fc_lock = flight_command
        self.vc_send, self.vc_recv, self.vc_lock = vehicle_command
        self.log_q = log_q
        self.module_name = self.__class__.__name__
        # TODO should verify that all flight path commands are valid on start up (just check attr on all autopilot methods)

    def run(self):
        while True:
            # TODO should move running of a flight path to be a method that can be called from flight command etc
            # TODO flight_path.txt in proper location?
            with open('flight_path.txt', 'r') as f:
                for command in f:
                    with self.vc_lock:
                        self.vc_send.send(command)
                    while True:
                        # TODO change
                        with self.vc_recv_lock:
                            response = self.vc_recv.recv()
                            # TODO check response successful or raise exception
            f.close()
            # TODO allow changes from interface
            # TODO send commands through vehicle_command pipe - synchronous communication
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
            sleep(600)
