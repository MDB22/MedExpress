from autopilot import *
from mission_reader import *

# IP address of vehicle
device = "127.0.0.1:14551"
#device = "com6"

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
