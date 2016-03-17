from autopilot import *
from mission_reader import *

# Address of vehicle
# IP for local host testing via UDP
device = "127.0.0.1:14551"
# Connection string for communicating to PixHawk via telemetry radio
#device = "com6"
# Connection string for communication to PixHawk via USB

# Name of KMZ file
filename = 'sample_mission.kmz'

# Process KMZ file
mission_info = GenerateMission(filename)

# Connect to the autopilot
pixhawk = Autopilot(device, mission_info, None, None)

# Activate the processes
pixhawk.start()

# About to exit script, make sure we cleanup

print("Mission complete.")
