# Module for controlling and interfacing with the LiDAR system, which is
# made up of two servos (pan and tilt) and LiDAR sensor

import os
import multiprocessing
import numpy as np

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
MIN_WIDTH = 1000
MAX_WIDTH = 2300

# Servo angle limits
MIN_ANGLE = 0
MAX_ANGLE = 180

# Angle increment for different scan resolutions
ANGLE_INC = 5

# Resolution of scans (at 5o increments)
NUM_POINTS_PER_PAN = 148
NUM_POINTS_PER_TILT = 37

# LiDAR poll frequency in Hz
FREQ = 65

# Linear map from desired angle to control value
def map(value, in_low, in_high, out_low, out_high):
        # Convert the initial value into a 0-1 range (float)
        valueScaled = (value - in_low) / float(in_high - in_low)

        # Convert the 0-1 range into a value in the new range.
        return out_low + valueScaled * (out_high - out_low)

class LidarSystem(multiprocessing.Process):
    
    def __init__(self):
        # Call superclass init
        super(LidarSystem, self).__init__()
        
        # Need to kill the process if it is already running, or we can't
        # create a new one or change parameters
        os.system('sudo killall servod -q')
        
        # Create a new servo process
        os.system('sudo ' + PATH + 'servod --step-size=' + 
            str(STEP_SIZE) + 'us ' + '--p1pins=' + PINS)
        
        # Open pipe to GPIO
        self.pipe = open(SERVO_PIPE,'w')
        
        # Create servo controllers for pan and tilt
        self.pan = ServoControl(1)
        self.tilt = ServoControl(0)
        
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
        except IOError as e:
            print e
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
        up = True
        
        while True:
            for angle in range(MIN_ANGLE, MAX_ANGLE+1, ANGLE_INC):
                # Move tilt servo
                self.setAngle(self.tilt, angle)
                
                if up:
                    # Sweep in one direction
                    data.append(self.sweep(MIN_ANGLE, MAX_ANGLE+1))
                else:
                    # Sweep the other direction
                    data.append(self.sweep(MAX_ANGLE, MIN_ANGLE-1))
                    
                # Change direction
                up = not up
            
        # TODO: Dump data to log file
    
    # Sweeps pan servo across its arc
    def sweep(self, start, end):
        data = []
        angles = []
        
        if start < end:
            angles = range(start, end, ANGLE_INC)
        else:
            angles = range(start, end, -ANGLE_INC)
            
        for angle in angles:
            self.setAngle(self.pan, angle)
            data.append(self.lidar.getRange())
            print data[-1]
        
        print "Length is" + str(len(data))
        return data
        
    # Run method for Process, performs in-flight, low-res scan
    def run(self):
        # 2D array for scans, initialised to "error" value of -1
        data = np.zeros((NUM_POINTS_PER_TILT, NUM_POINTS_PER_PAN), dtype=float) - 1
        
        # Control for changing direction of sweep
        pan_direction = -1
        tilt_direction = -1
        
        # Counters for indexing array
        pan_index = 0
        tilt_index = 0
        
        # Start both servos at close to 0
        pan_angle = 0
        tilt_angle = 0
        
        # Offset to get overlapping scans
        pan_offset = 1.25
        
        # Initialise servos
        self.setAngle(self.pan, pan_angle)
        self.setAngle(self.tilt, tilt_angle)
        data[tilt_index, pan_index] = self.lidar.getRange()
                
        while True:
            # If tilt exceeds limit, reverse direction
            if tilt_angle >= 180 or tilt_angle <= 0:
                tilt_direction *= -1
            
            # If pan exceeds limit, reverse direction
            if pan_angle >= 180 or pan_angle <= 0:
                pan_direction *= -1
            
            pan_angle += pan_direction * ANGLE_INC/float(4)             
            pan_index += pan_direction 
                
            tilt_angle += tilt_direction * ANGLE_INC                
            tilt_index += tilt_direction 
            
            self.setAngle(self.pan, pan_angle)
            self.setAngle(self.tilt, tilt_angle)
            data[tilt_index, pan_index] = self.lidar.getRange()
            
            print "Pan at " + str(pan_angle)
            print "Tilt at " + str(tilt_angle)
            print "Just read: " + str(data[tilt_index, pan_index])
            
            