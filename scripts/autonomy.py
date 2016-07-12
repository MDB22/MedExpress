
from flight import *
from command import *
from sensing import *
from ground_station import *
from autopilot import *

import argparse

# Setup command line arguments
parser = argparse.ArgumentParser(description='Executes autonomous mission on a UAV.')
parser.add_argument('--connection-type', dest='device', required=True,
	choices=['udp', 'telemetry', 'usb-windows', 'usb-linux', 'serial'],
	help='Device to connect to for flight commands')

args = parser.parse_args()
device = args.device

# Set connection address to communicate with vehicle
if device == 'udp':
	# Connection string for communication to Pixhawk via UDP
	device_address = '127.0.0.1:14551'
elif device == 'telemetry' or device == 'usb-windows':
	# Connection string for communicating to Pixhawk via telemetry radio, or USB (Windows)
	device_address = 'com6'
elif device == 'usb-linux':
	# Connection string for communication to Pixhawk via USB (Linux)
	device_address = '/dev/ttyUSB0'
else:
	# Connection string for communication to Pixhawk via serial port (Linux)
	device_address = '/dev/ttyAMA0'

# Name of KMZ file
filename = 'sample_mission.kmz'

# Process KMZ file
mission_info = GenerateMission(filename)

# Connect to the autopilot
pixhawk = Autopilot(device_address, mission_info, None, None)

# Activate the processes
pixhawk.start()

# About to exit script, make sure we cleanup

print('Mission complete.')
