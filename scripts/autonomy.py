from autopilot import *
from mission_reader import *

# IP address of vehicle
ip = "127.0.0.1:14551"

# Name of KMZ file
filename = 'sample_mission.kmz'

# Process KMZ file
mission_info = GenerateMission(filename)

# Connect to the autopilot
pixhawk = Autopilot(ip, mission_info, None, None)

# Activate the processes
pixhawk.start()

# About to exit script, make sure we cleanup

print("Mission complete.")
