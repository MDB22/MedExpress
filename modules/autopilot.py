import multiprocessing
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil
import time
from logging import Log

class Autopilot(multiprocessing.Process):
    ARM_TIMEOUT = 20
    GPS_NO_FIX = [0,1] # 0,1 = No fix, 2 = 2D fix, 3 = 3D fix

    def __init__(self, api, vehicle_command, log_q):
        super(Autopilot, self).__init__()
        self.api = api
        self.vehicle = api.get_vehicles()[0]
        self.vehicle_command = vehicle_command
        self.log_q = log_q
        self.armed = False

    def takeoff(self, altitude):
        """ fly to altitude
        :param altitude: int (in meters)
        :return:
        """
        if not self.armed:
            # TODO wrap in try
            self.arm()



    def arm(self):
        """ Arm the uav
        :return: None
        """
        # TODO should check / raise exception on arm failure
        # check we have booted and have GPS
        # TODO exception on timeout amount
        while self.vehicle.mode.name == "INITIALISING":
            print "Waiting for vehicle to initialise" # TODO msg over log
            time.sleep(1)
        while self.vehicle.gps_0.fix_type in GPS_NO_FIX:
            print "Waiting for GPS" # TODO msg over log
            time.sleep(1)

        # arm vehicle in guided mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True
        self.vehicle.flush()

        # api.exit is set true by mavproxy when connection finished
        while not vehicle.armed and not self.api.exit:
            print " Waiting for arming..." # TODO msg over log
            time.sleep(1)
        self.armed = True

    def disarm(self):
        """ Disarm the uav
        :return: None
        """
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = False
        self.vehicle.flush()
        self.armed = False

    def run(self):
        while True:
            pass