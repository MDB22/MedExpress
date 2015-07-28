# Module for controlling and interfacing with the LiDAR system, which is
# made up of two servos (pan and tilt) and LiDAR sensor

import os
import multiprocessing
import pickle
import numpy as np

from servoControl import * 
from lidar import *

# Path to ServoBlaster process, need to make generic to each user
PIPE_PATH = '/home/mdb/ServoBlaster/'
WRITE_PATH = '../tests/'

# Step size of 2us to allow more accurate scans
STEP_SIZE = 2

# List of pins being used by servos, using pin order numbering
PINS = '7,11'

# Linux pipe used to issue commands to GPIO
SERVO_PIPE = '/dev/servoblaster'

# Limits for servo controls in microseconds, approximate 180o arc
MIN_WIDTH_PAN = 600
MAX_WIDTH_PAN = 2300
MIN_WIDTH_TILT = 1150
MAX_WIDTH_TILT = 2300

# Servo angle limits
MIN_ANGLE_PAN = 0
MAX_ANGLE_PAN = 180
MIN_ANGLE_TILT = 80
MAX_ANGLE_TILT = 180

# Angle increment for different scan resolutions
ANGLE_INC = 5

# Resolution of scans (at 5o increments)
NUM_POINTS_PER_PAN = 37
NUM_POINTS_PER_TILT = 81

# LiDAR poll frequency in Hz
FREQ = 65

class LidarSystem(multiprocessing.Process):
    
    def __init__(self):
        # Call superclass init
        super(LidarSystem, self).__init__()
        
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
        self.pan = ServoControl(0, 'pan', pan_limits)
        self.tilt = ServoControl(1, 'tilt', tilt_limits)
        
        # Create lidar object
        self.lidar = Lidar(FREQ)        
        
        # 2D array for scans, initialised to NaN
        self.data = np.zeros((NUM_POINTS_PER_TILT, NUM_POINTS_PER_PAN), dtype=float)*np.NaN
        self.all_data = []
        
    def __del__(self):  
        self.cleanup()
        
    def cleanup(self):        
        # Kill the servo process during cleanup
        import os
        print "Killing servo process"
        os.system('sudo killall servod -q')   
    
    # Performs raster scan with LiDAR
    def scan(self):
        data = []
        up = True
        
        while True:
            for angle in range(MIN_ANGLE, MAX_ANGLE+1, ANGLE_INC):
                # Move tilt servo
                self.tilt.setAngle(self.pipe,angle)
                
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
            self.pan.setAngle(self.pipe,angle)
            data.append(self.lidar.getRange())
            print data[-1]
        
        print "Length is" + str(len(data))
        return data
        
    # Run method for Process, performs in-flight, low-res scan
    def run(self):
        # Counts number of data arrays written
        data_count = 0
        
        # Control for changing direction of sweep
        pan_direction = -1
        tilt_direction = -1
        
        # Counters for indexing array
        pan_index = 0
        tilt_index = 0
        
        # Start both servos at close to 0
        pan_angle = MIN_ANGLE_PAN
        tilt_angle = MIN_ANGLE_TILT
        
        # Offset to get overlapping scans
        pan_offset = 1.25
        
        # Initialise servos
        self.pan.setAngle(self.pipe,pan_angle)
        self.tilt.setAngle(self.pipe,tilt_angle)
        self.data[tilt_index, pan_index] = self.lidar.getRange()
        
        while True:
            # If tilt exceeds limit, reverse direction
            if tilt_angle <= MIN_ANGLE_TILT or tilt_angle >= MAX_ANGLE_TILT:
                tilt_direction *= -1
                print tilt_index
                print "Appending array " + str(data_count)
                self.all_data.append(self.data)
                self.data = np.zeros((NUM_POINTS_PER_TILT, NUM_POINTS_PER_PAN), dtype=float)*np.NaN
                data_count += 1
                
                if data_count == 30:   
                    data_count = 0
                    # Write data to file
                    print "Pickling data"
                    data_out = open(WRITE_PATH + 'data.out', 'w')
                    pickle.dump(self.all_data, data_out)
                    data_out.close()
                    return
              
            # If pan exceeds limit, reverse direction
            if pan_angle <= MIN_ANGLE_PAN or pan_angle >= MAX_ANGLE_PAN:
                pan_direction *= -1
                
            pan_angle += pan_direction * ANGLE_INC            
            pan_index += pan_direction 
                 
            tilt_angle += tilt_direction * ANGLE_INC/4.      
            tilt_index += tilt_direction 
                
            self.pan.setAngle(self.pipe,pan_angle)
            self.tilt.setAngle(self.pipe,tilt_angle)
            d = self.lidar.getRange()
            self.data[tilt_index, pan_index] = d
                
            #print "Pan at " + str(pan_angle)
            #print "Tilt at " + str(tilt_angle)
            #print "Just read: " + str(data[tilt_index, pan_index])            
            
if __name__ == '__main__':            
    l = LidarSystem()
    l.start()
    
    time.sleep(60)
    
    l.join()
    
    print "Unpickling"
    import pickle
    data_in = open(WRITE_PATH + 'data.out')
    data = pickle.load(data_in)
    print data
    i = 0
    for d in data:
    	    np.savetxt(WRITE_PATH + 'data' + str(i) + '.csv',np.asarray(d),'%3.2f',',')
    	    i += 1