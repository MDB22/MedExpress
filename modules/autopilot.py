import multiprocessing
import exceptions
import socket
import time

from dronekit import *

#from pymavlink import mavutil
#from time import sleep
#from uav_logging import *

###
# Use droneapi Callbacks to monitor vehicle state
# Use on_message('COMMAND_ACK') and on_message('STATUSTEXT') to monitor MAVLink messages
# Use the system_status attribute to monitor vehicle status using Drone Kit
# Use MAV_CMD_DO_FLIGHTTERMINATION for emeergency stop
# Use param set SIM_GPS_DISABLE 1 in MAVProxy to test GPS failure
###

class Autopilot():
    ARM_TIMEOUT = 20
    GPS_NO_FIX = [0,1] # 0,1 = No fix, 2 = 2D fix, 3 = 3D fix
    LOC_ACCURACY = 0.95

    def __init__(self, device, mission_info, vehicle_command, log_q):
        
        self.vehicle = self.connectToVehicle(device)
        self.setHomeLocation(mission_info['base_location'][0])
        
        # Potentially incorrect ordering here, main passes tuple of (Pipe, Lock, Lock)
        #self.vc_send, self.vc_recv, self.vc_lock = vehicle_command
        self.log_q = log_q
        self.module_name = self.__class__.__name__

    def connectToVehicle(self, device):
        print("Connecting to " + device)

        # Connect to vehicle, be on the look out for failures
        try:
            vehicle = connect(device, heartbeat_timeout=15, wait_ready=True, baud=57600)
            return vehicle
        # Bad TCP connection
        except socket.error:
            print("No server exists!")
        except APIException:
            print("Timeout!")
        # Bad TTY connection
        except exceptions.OSError as e:
            print("No serial exists!")
        # Other error
        except:
            print("Something else went wrong!")

    # Sets the vehicle's home location to be the base
    # position defined in the KMZ file.
    def setHomeLocation(self, location):
        cmds = self.vehicle.commands
        cmds.download()
        cmds.wait_ready()
        print(self.vehicle.home_location)

        # Set base location
        # Can only set location if there is a GPS fix
##        self.vehicle.home_location = LocationGlobal(location['lat'],\
##                                                             location['long'],\
##                                                             location['alt'])

        print(location)
        print(self.vehicle.home_location)

    # Starts the vehicle's mission, as defined by the KMZ file
    def start(self):
        while False:
            # read and execute commands off vehicle_command pipe
            with self.vc_lock:
                command = self.vc_recv.recv().split()
                # TODO exception on failed calls
                # command syntax: method param1 param2 ...
                # call the method with given parameters using getattr
                response = getattr(self, command[0])(*command[1:])
                # TODO change
                with self.vc_send_lock:
                    self.vc_send.send(response)
            sleep(1)

        # Arm the vehicle
        self.arm()
        self.takeoff(10)
        self.disarm()
        self.vehicle.close()

    # Arms the vehicle, but only if safe to do so
    def arm(self):
        """ Arm the uav
        :return: None
        """
        
        # TODO should check / raise exception on arm failure
        # check we have booted and have GPS
        # TODO exception on timeout amount
        
        # Don't try to arm until autopilot is ready
##        while not self.vehicle.is_armable:
##            print " Waiting for vehicle to initialise..."
##            time.sleep(1)
        
##        while self.vehicle.gps_0.fix_type in self.GPS_NO_FIX:
##            print "Waiting for GPS" # TODO msg over log
##            time.sleep(1)
            
        print "Arming motors"
        # Copter should arm in GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True    

        # Confirm vehicle armed before attempting to take off
        while not self.vehicle.armed:      
            print " Waiting for arming..."
            time.sleep(1)

    def disarm(self):
        """ Disarm the uav
        :return: None
        """
        self.vehicle.armed = False
        self.vehicle.flush()
        # set to stabilize for manual control
        self.vehicle.mode = VehicleMode("STABILIZE")

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

        self.vehicle.simple_takeoff(altitude)
        
        # todo should catch connection lost as exception
##        while not self.api.exit:
##            print " Altitude: ", self.vehicle.location.alt
##            # if close to set point return
##            if self.vehicle.location.alt>=altitude*self.LOC_ACCURACY:
##                return True
##            time.sleep(1)
            
        time.sleep(10)

    # Commands the aircraft to switch between rotor and fixed-wing flight
    def transition(self):
        pass
        # Send transition command to aircraft, somehow change flight configuration

        # Set Geofence on transition
