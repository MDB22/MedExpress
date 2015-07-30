
from uav_state import *
from world_state import *
from interface import *
from logging import *
from flight import *
from autopilot import *

import multiprocessing
from multiprocessing.managers import BaseManager
#from droneapi.lib import VehicleMode
#from pymavlink import mavutil

# First get an instance of the API endpoint
# todo reenable
#api = local_connect()
# Get the connected vehicle (currently only one vehicle can be returned).
#vehicle = api.get_vehicles()[0]
api = "test"

# Create shared queues and pipes
log_q = multiprocessing.Queue()

flight_command = multiprocessing.Pipe()
fc_send_lock = multiprocessing.Lock()
fc_recv_lock = multiprocessing.Lock()
flight_command += (fc_send_lock, fc_recv_lock)

vehicle_command = multiprocessing.Pipe()
vc_send_lock = multiprocessing.Lock()
vc_recv_lock = multiprocessing.Lock()
vehicle_command += (vc_send_lock, vc_recv_lock)

# Shared memory for state objects
class StateManager(BaseManager): pass
StateManager.register('UavState', UavState)
StateManager.register('WorldState', WorldState)
state_manager = StateManager()
state_manager.start()
uav_state = state_manager.UavState()
world_state = state_manager.WorldState()

# Create objects for process modules
uav_state_updater = UavStateUpdater(uav_state, vehicle, log_q)
world_state_updater = WorldStateUpdater(world_state, log_q)
interface = Interface(flight_command, log_q)
logging = Logging(log_q)
autopilot = Autopilot(api, vehicle_command, log_q)
flight = Flight(uav_state, world_state, flight_command, vehicle_command, log_q)

# TODO uncaught error / exception from on of these process should initiate emergency mode
# Start processes
uav_state_updater.start()
world_state_updater.start()
interface.start()
logging.start()
autopilot.start()
flight.start()

# Wait for processes to finish
uav_state_updater.join()
world_state_updater.join()
interface.join()
logging.join()
autopilot.join()
flight.join()