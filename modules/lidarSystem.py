# Module for controlling and interfacing with the LiDAR system, which is
# made up of two servos (pan and tilt) and LiDAR sensor

import os
import csv
import math
import time
import pickle
import multiprocessing
import numpy as np

from numpy import sin, cos
from servoControl import * 
from lidar import *

# Path to ServoBlaster process, need to make generic to each user
PIPE_PATH = '/home/' + os.getlogin() + '/ServoBlaster/'
WRITE_PATH = '/home/' + os.getlogin() + '/med_express_uav/tests/'

# Step size of 2us to allow more accurate scans
STEP_SIZE = 2

# List of pins being used by servos, using pin order numbering
PINS = '7,11'

# Linux pipe used to issue commands to GPIO
SERVO_PIPE = '/dev/servoblaster'

# Limits for servo controls in microseconds, approximate 180o arc
MIN_WIDTH_PAN = 650
MAX_WIDTH_PAN = 2400
MIN_WIDTH_TILT = 600
MAX_WIDTH_TILT = 1760

# Servo angle limits
MIN_ANGLE_PAN = -85
MAX_ANGLE_PAN = 85
MIN_ANGLE_TILT = -90
MAX_ANGLE_TILT = 20

# Angle increment for different scan resolutions
ANGLE_INC = 5

# Number of pan scans in each tilt scan
SPEED_RATIO = 4

# Resolution of scans (at 5 degree increments)
NUM_POINTS_PER_PAN = (MAX_ANGLE_PAN - MIN_ANGLE_PAN)/ANGLE_INC + 1
NUM_POINTS_PER_TILT = SPEED_RATIO*(MAX_ANGLE_TILT - MIN_ANGLE_TILT)/ANGLE_INC + 1

# LiDAR poll frequency in Hz
FREQ = 65

# Offset distances and angles to convert from LiDAR frame to UAV frame
OFFSET_TO_SERVO_TX = 0.5
OFFSET_TO_SERVO_TZ = 2.1

OFFSET_TO_PAN_TX = 3.5
OFFSET_TO_PAN_TZ = 2.5

OFFSET_TO_PIXHAWK = 35

class LidarSystem(multiprocessing.Process):
    
    def __init__(self, period, queue):
        # Call superclass init
        super(LidarSystem, self).__init__()
        
        # Store the period (in milliseconds) for pushing to the queue
        self.period = period
        
        # Need to kill the process if it is already running, or we can't
        # create a new one or change parameters
        os.system('sudo killall servod -q')
        
        # Create a new servo process
        os.system('sudo ' + PIPE_PATH + 'servod --step-size=' + 
            str(STEP_SIZE) + 'us ' + '--p1pins=' + PINS)
        
        # Open pipe to GPIO
        self.pipe = open(SERVO_PIPE,'w')

        # Tuples for passing to servo objects
        pan_limits = (MIN_ANGLE_PAN, MAX_ANGLE_PAN, MIN_WIDTH_PAN, MAX_WIDTH_PAN)
        tilt_limits = (MIN_ANGLE_TILT, MAX_ANGLE_TILT, MIN_WIDTH_TILT, MAX_WIDTH_TILT)
        
        # Create servo controllers for pan and tilt, pass limit values
        self.pan = ServoControl(0, 'pan', pan_limits, self.pipe)
        self.tilt = ServoControl(1, 'tilt', tilt_limits, self.pipe)
        
        # Create lidar object
        self.lidar = Lidar(FREQ)        
        
        # 2D array for scans, initialised to NaN
        self.data = np.zeros((NUM_POINTS_PER_TILT, NUM_POINTS_PER_PAN), dtype=float)*np.NaN
        self.all_data = []
        
        # Store the queue object to communicate with the other processes
        self.queue = queue
        
    def __del__(self):  
        self.cleanup()
        
    def cleanup(self):        
        # Kill the servo process during cleanup
        import os
        print "Killing servo process"
        os.system('sudo killall servod -q')   

    # Converts a LiDAR distance measurement to a vector in the UAV frame 
    def toUAVFrame(self, pan_deg, tilt_deg, distance):
        
        # Convert degrees to radians for numpy methods
        pan = np.radians(pan_deg)
        tilt = np.radians(tilt_deg)
        
        # Convert directly to distance vecotr, with origin at PixHawk
        vec = np.array([
                OFFSET_TO_PAN_TZ*cos(pan) + OFFSET_TO_SERVO_TZ*cos(pan)*cos(tilt) -
            OFFSET_TO_SERVO_TX*cos(pan)*sin(tilt) + cos(pan)*cos(tilt)*distance
            + OFFSET_TO_PIXHAWK,
                OFFSET_TO_PAN_TZ*sin(pan) + OFFSET_TO_SERVO_TZ*cos(tilt)*sin(pan) -
            OFFSET_TO_SERVO_TX*sin(pan)*sin(tilt) + sin(pan)*cos(tilt)*distance,
                -OFFSET_TO_SERVO_TX*cos(tilt) - OFFSET_TO_SERVO_TZ*sin(tilt) 
            - distance*sin(tilt) - OFFSET_TO_PAN_TX
        		])
        
        return vec[0:3]
    
    # Performs raster scan with LiDAR
    def scan(self):
        data = []
        up = True
        
        while True:
            for angle in range(MIN_ANGLE, MAX_ANGLE+1, ANGLE_INC):
                # Move tilt servo
                self.tilt.setAngle(angle)
                
                if up:
                    # Sweep in one direction
                    data.append(self.sweep(MIN_ANGLE, MAX_ANGLE+1))
                else:
                    # Sweep the other direction
                    data.append(self.sweep(MAX_ANGLE, MIN_ANGLE-1))
                    
                # Change direction
                up = not up
                
    # Sweeps pan servo across its arc
    def sweep(self, start, end):
        data = []
        
        if start < end:
            angles = range(start, end, ANGLE_INC)
        else:
            angles = range(start, end, -ANGLE_INC)
            
        for angle in angles:
            self.pan.setAngle(angle)
            data.append(self.lidar.getRange())
            print data[-1]
        
        print "Length is" + str(len(data))
        return data
        
    # Run method for Process, performs in-flight, low-res scan
    def run(self):
    	# Timer for updating UAV parameters
    	timer = 0
    	    
        # Counts number of data arrays written
        data_count = 0
        
        # Control for changing direction of sweep
        pan_direction = -1
        tilt_direction = -1
        
        # Counters for indexing array
        pan_index = 0
        tilt_index = 0
        
        # Start both servos at close at minimum angle
        pan_angle = MIN_ANGLE_PAN
        tilt_angle = MIN_ANGLE_TILT
        
        # Initialise servos
        
        while True:
            # Update timer
            timer = time.time()
            
            # Update servos
            self.pan.setAngle(pan_angle)
            self.tilt.setAngle(tilt_angle)
            
            # Get data and transform it to the UAV coordinate frame
            self.all_data.append(self.toUAVFrame(
                pan_angle, tilt_angle, self.lidar.getRange()))
            
            # If tilt exceeds limit, reverse direction
            if tilt_angle <= MIN_ANGLE_TILT or tilt_angle >= MAX_ANGLE_TILT:
                tilt_direction *= -1
                data_count += 1
              
            # If pan exceeds limit, reverse direction
            if pan_angle <= MIN_ANGLE_PAN or pan_angle >= MAX_ANGLE_PAN:
                pan_direction *= -1
                
            pan_angle += pan_direction * ANGLE_INC            
            pan_index += pan_direction 
                 
            tilt_angle += tilt_direction * ANGLE_INC/4.      
            tilt_index += tilt_direction       
            
            # If we have exceeded the period, push our data to the queue        
            if (time.time() - timer > self.period):
                print "Pushing to Queue"
                self.queue.put(self.all_data)
                timer = time.time()

