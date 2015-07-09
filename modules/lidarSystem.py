import os

from servoControl import * 

# Path to ServoBlaster process, need to make generic to each user
PATH = '/home/mdb/ServoBlaster/'

# Step size of 2us to allow more accurate scans
STEP_SIZE = 2

# List of pins being used by servos, using pin order numbering
PINS = '7'

# Linux pipe used to issue commands to GPIO
SERVO_PIPE = '/dev/servoblaster'

# Limits for servo controls in microseconds, approximate 180o arc
MIN_ANGLE = 600
MAX_ANGLE = 2300

# Linear map from desired angle to control value
def map(value, in_low, in_high, out_low, out_high):
        # Convert the initial value into a 0-1 range (float)
        valueScaled = (value - in_low) / float(in_high - in_low)

        # Convert the 0-1 range into a value in the new range.
        return out_low + valueScaled * (out_high - out_low)

class PanTiltControl:
	
	def __init__(self):
		# Need to kill the process if it is already running, or we can't
		# create a new one or change parameters
		os.system('sudo killall servod -q')
		
		# Create a new servo process
		os.system('sudo ' + PATH + 'servod --step-size=' + 
			str(STEP_SIZE) + 'us ' + '--p1pins=' + PINS)
		
		# Open pipe to GPIO
		self.pipe = open(SERVO_PIPE,'w')
		
		self.pan = ServoControl(0)
		self.tilt = ServoControl(1)
		
	def __del__(self):
		# Kill the servo process during cleanup
		os.system('sudo killall servod -q')
	