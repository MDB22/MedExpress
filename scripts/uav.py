
from uav_state import *
from world_state import *
from interface import *
from logging import *
from flight import *
from autopilot import *
from log import *

import multiprocessing
from multiprocessing.managers import BaseManager
from droneapi.lib import VehicleMode
from pymavlink import mavutil

# First get an instance of the API endpoint
api = local_connect()
# Get the connected vehicle (currently only one vehicle can be returned).
vehicle = api.get_vehicles()[0]

# Create shared queues and pipes
log_q = multiprocessing.Queue()
flight_command_p = multiprocessing.Pipe() # Need to lock when read / writing to this
vehicle_command_p = multiprocessing.Pipe() # Need to lock when read / writing to this

# Shared memory for state objects
class StateManager(BaseManager): pass
StateManager.register('UavState', UavState) #TODO set to only expose read functions
StateManager.register('WorldState', WorldState) #TODO set to only expose read functions
state_manager = StateManager()
state_manager.start()
uav_state = state_manager.UavState(log_q)
world_state = state_manager.WorldState(log_q)

# Create objects for process modules
uav_state_updater = UavStateUpdater(uav_state, vehicle, log_q)
world_state_updater = WorldStateUpdater(world_state, log_q)
interface = Interface(flight_command_p, log_q)
logging = Logging(log_q)
autopilot = Autopilot(vehicle, vehicle_command_p, log_q)
flight = Flight(uav_state, world_state, flight_command_p, vehicle_command_p, log_q)

# Start processes
uav_state_updater.start()
world_state_updater.start()
interface.start()
logging.start()
autopilot.start()
flight.start()
