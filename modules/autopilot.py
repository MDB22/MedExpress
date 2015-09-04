import multiprocessing
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil
from time import sleep
from uav_logging import *

class Autopilot():
    ARM_TIMEOUT = 20
    GPS_NO_FIX = [0,1] # 0,1 = No fix, 2 = 2D fix, 3 = 3D fix
    LOC_ACCURACY = 0.95

    def __init__(self, api, vehicle_command, log_q):
        self.api = api
        self.vehicle = api.get_vehicles()[0]
        self.vc_send, self.vc_recv, self.vc_send_lock, self.vc_recv_lock = vehicle_command
        self.log_q = log_q
        self.module_name = self.__class__.__name__

    def takeoff(self, altitude):
        """ fly to altitude
        :param altitude: int (in meters)
        :return: boolean (reached altitude)
        """
        # convert command string
        altitude = float(altitude)
        if not self.vehicle.armed:
            # TODO wrap in try
            self.arm()

        self.vehicle.commands.takeoff(altitude)
        self.vehicle.flush()
        # todo should catch connection lost as exception
        while not self.api.exit:
            print " Altitude: ", self.vehicle.location.alt
            # if close to set point return
            if self.vehicle.location.alt>=altitude*self.LOC_ACCURACY:
                return True
            time.sleep(1)
        # TODO proper return check
        return "SUCCESS"

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
        while self.vehicle.gps_0.fix_type in self.GPS_NO_FIX:
            print "Waiting for GPS" # TODO msg over log
            time.sleep(1)

        # Make sure we are in guided mode for programmatic control
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True
        self.vehicle.flush()
        # Check that arming has completed
        while not self.vehicle.armed and not self.api.exit:
            print " Waiting for arming..." # TODO msg over log
            time.sleep(1)

    def disarm(self):
        """ Disarm the uav
        :return: None
        """
        self.vehicle.armed = False
        self.vehicle.flush()
        # set to stabilize for manual control
        self.vehicle.mode = VehicleMode("STABILIZE")

    def start(self):
        while True:
            # read and execute commands off vehicle_command pipe
            with self.vc_recv_lock:
                command = self.vc_recv.recv().split()
                # todo exception on failed calls
                # command syntax: method param1 param2 ...
                response = getattr(self, command[0])(*command[1:])
                with self.vc_send_lock:
                    self.vc_send.send(response)
            sleep(1)
