# Module for controlling and interfacing with the LiDAR system, which is
# made up of two servos (pan and tilt) and LiDAR sensor

import os

from servoControl import * 
from lidar import *

# Path to ServoBlaster process, need to make generic to each user
PATH = '/home/mdb/ServoBlaster/'

# Step size of 2us to allow more accurate scans
STEP_SIZE = 2

# List of pins being used by servos, using pin order numbering
PINS = '7,11'

# Linux pipe used to issue commands to GPIO
SERVO_PIPE = '/dev/servoblaster'

# Limits for servo controls in microseconds, approximate 180o arc
MIN_WIDTH = 600
MAX_WIDTH = 2300

# Servo angle limits
MIN_ANGLE = 0
MAX_ANGLE = 180

# LiDAR poll frequency in Hz
FREQ = 100

# Linear map from desired angle to control value
def map(value, in_low, in_high, out_low, out_high):
        # Convert the initial value into a 0-1 range (float)
        valueScaled = (value - in_low) / float(in_high - in_low)

        # Convert the 0-1 range into a value in the new range.
        return out_low + valueScaled * (out_high - out_low)

class LidarSystem:
	
	def __init__(self):
		# Need to kill the process if it is already running, or we can't
		# create a new one or change parameters
		os.system('sudo killall servod -q')
		
		# Create a new servo process
		os.system('sudo ' + PATH + 'servod --step-size=' + 
			str(STEP_SIZE) + 'us ' + '--p1pins=' + PINS)
		
		# Open pipe to GPIO
		self.pipe = open(SERVO_PIPE,'w')
		
		# Create servo controllers for pan and tilt
		self.pan = ServoControl(0)
		self.tilt = ServoControl(1)
		
		# Create lidar object
		self.lidar = Lidar(FREQ)
		
	def __del__(self):
		# Kill the servo process during cleanup
		os.system('sudo killall servod -q')
	
	# Set the angle of only the pan servo (debug purposes)
	def setPanAngle(self, angle):
		self.setAngle(self.pan, angle)
		
	# Set the angle of only the tilt servo (debug purposes)
	def setTiltAngle(self, angle):
		self.setAngle(self.tilt, angle)
	
	# Set the angle of a servo
	def setAngle(self, servo, angle):
		
		pulseWidth = map(angle, MIN_ANGLE, MAX_ANGLE, MIN_WIDTH, MAX_WIDTH)
		
		try:
			self.sendCommand(servo, pulseWidth)
		except IOError:
			print 'Cannot move to the desired angle: ' + str(angle)
	
	# Send the angle command in microseconds to the servo
	def sendCommand(self, servo, width):
		# Throw exception if angle is not valid
		if (width < MIN_WIDTH or width > MAX_WIDTH):
			raise IOError()
			
		servo.setPosition(self.pipe, width)
	
	# Performs raster scan with LiDAR
	def scan(self):
		data = []
		while True:
			for angle in range(MIN_ANGLE, MAX_ANGLE+1):
				# Move tilt servo
				self.setAngle(self.tilt, angle)
				# Sweep in one direction
				data.append(self.sweep(MIN_ANGLE, MAX_ANGLE+1))
				# Sweep the other direction
				data.append(self.sweep(MAX_ANGLE, MIN_ANGLE-1))
			
		# TODO: Dump data to log file
	
	# Sweeps pan servo across its arc
	def sweep(self, start, end):
		data = []
		angles = []
		
		if start < end:
			angles = range(start, end)
		else:
			angles = range(start, end, -1)
			
		for angle in angles:
			self.setAngle(self.pan, angle)
			data.append(self.lidar.getRange())
			print data[-1]
		
		return data