from autopilot import *
from mission_reader import *

# IP address of vehicle
ip = "tcp:127.0.0.1:5760"

# Name of KMZ file
filename = 'sample_mission.kmz'

# Process KMZ file
kml = GenerateMission()

# Connect to the autopilot
pixhawk = Autopilot(ip, None, None)

# Activate the processes
pixhawk.start()

# About to exit script, make sure we cleanup

print("Mission complete.")
