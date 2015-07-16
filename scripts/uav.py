
from uav_state import *
from world_state import *
from interface import *
from logging import *
from flight import *
from autopilot import *

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
flight_command_p = multiprocessing.Pipe()
vehicle_command_p = multiprocessing.Pipe()

# Shared memory for state objects
class StateManager(BaseManager): pass
StateManager.register('UavState', UavState)
StateManager.register('WorldState', WorldState)
state_manager = StateManager()
state_manager.start()
uav_state = state_manager.UavState()
world_state = state_manager.WorldState()

# Create objects for process modules
uav_state_updater = UavStateUpdater(uav_state, vehicle)
world_state_updater = WorldStateUpdater(world_state)
interface = Interface(flight_command_p)
logging = Logging(log_q)
autopilot = Autopilot(vehicle, vehicle_command_p)
flight = Flight(uav_state, world_state, flight_command_p, vehicle_command_p)

# Start processes
uav_state_updater.start()
world_state_updater.start()
interface.start()
logging.start()
autopilot.start()
flight.start()
