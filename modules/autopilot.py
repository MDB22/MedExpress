import multiprocessing
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil
import time
from uav_logging import Log

class Autopilot():
    ARM_TIMEOUT = 20
    GPS_NO_FIX = [0,1] # 0,1 = No fix, 2 = 2D fix, 3 = 3D fix

    def __init__(self, api, vehicle_command, log_q):
        self.api = api
        self.vehicle = api.get_vehicles()[0]
        self.vehicle_command = vehicle_command
        self.log_q = log_q
        self.armed = False #TODO remove and use vehicle.armed => not working with sitl?

    def takeoff(self, altitude):
        """ fly to altitude
        :param altitude: int (in meters)
        :return:
        """
        print self.vehicle.armed
        if not self.vehicle.armed:
            # TODO wrap in try
            self.arm()

        self.vehicle.commands.takeoff(altitude)
        self.vehicle.flush()
        while True:
            print " Altitude: ", self.vehicle.location.alt
            time.sleep(1)

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
        self.armed = True # TODO remove
        # Check that arming has completed # todo reenable on uav
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
        self.armed = False # TODO remove

    def start(self):
        while True:
            self.takeoff(20)