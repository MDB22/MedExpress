
from flight import *
from command import *
from sensing import *
from ground_station import *
from autopilot import *

import argparse

# Launches the UAV's mission
def run():

	device, mission_file = parse_args()

	# Set connection address to communicate with vehicle
	if device == 'udp':
		# Connection string for communication to Pixhawk via UDP
		device_address = '127.0.0.1:14551'
	elif device == 'sitl':
		# Connection string for communication with a headless SITL instance
		device_address = 'tcp:127.0.0.1:5760'
	elif device == 'telemetry' or device == 'usb-windows':
		# Connection string for communicating to Pixhawk via telemetry radio, or USB (Windows)
		device_address = 'com6'
	elif device == 'usb-linux':
		# Connection string for communication to Pixhawk via USB (Linux)
		device_address = '/dev/ttyUSB0'
	else:
		# Connection string for communication to Pixhawk via serial port (Linux)
		device_address = '/dev/ttyAMA0'

	# Process KMZ file
	mission_info = mission_reader.GenerateMission(mission_file)

	# Connect to the autopilot
	pixhawk = Autopilot(device_address, mission_info, None, None)

	# Activate the processes
	pixhawk.start()

	# About to exit script, make sure we cleanup
	pixhawk.join()

	print('Mission complete.')

# Processes command lne arguments to configure mission execution
def parse_args():
	# Setup command line arguments
	parser = argparse.ArgumentParser(description='Executes autonomous mission on a UAV.')
	parser.add_argument('--connection-type', dest='device', required=True,
		choices=['udp', 'sitl', 'telemetry', 'usb-windows', 'usb-linux', 'serial'],
		help='Device to connect to for flight commands')
	parser.add_argument('--mission-file', dest='mission', required=True,
		help='File path to locate mission KMZ file')

	args = parser.parse_args()

	device = args.device
	mission_file = args.mission

	return device, mission_file

if __name__ == "__main__":
	run()