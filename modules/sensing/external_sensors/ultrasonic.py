# Class for interfacing with the ultrasonic sensor

import RPi.GPIO as GPIO
import time
from numpy import array

# Pin associated with "triggering" the sensor
TRIG = 27
# Pin that returns data from sensor
ECHO = 22

# If measurement takes longer than this, we assume it has failed
WAIT_TIME = 0.5
# Error code, so we can try another pulse
ERROR = -1
# Big number, which indicates distance measurement has failed
FAILURE = 1.e8

# Offsets (cm) for converting to UAV frame
OFFSET_X = 2.
OFFSET_Z = 10.

class Ultrasonic:
    
    def __init__(self):
        # Use GPIO numbers, not pin numbers
        GPIO.setmode(GPIO.BCM)
        print "Set up Trigger as output"
        GPIO.setup(TRIG, GPIO.OUT)
        print "Set up Echo as input"
        GPIO.setup(ECHO, GPIO.IN)
        print "Set Trigger low"
        GPIO.output(TRIG, False)
        # May need to wait for sensor to settle
        #print "Waiting for sensor to settle"
        time.sleep(2)
        print "Initialisation complete, ultrasound ready"

    def __del__(self):
        GPIO.cleanup()

    def toUAVFrame(self, distance):
        # TODO: Need to make sure units match
        # TODO: Need to verify actual offsets
        return array([OFFSET_X, 0, distance + OFFSET_Z])
        
    def sendPulse(self):
    	try:
            # Trigger the ultrasound pulse
            GPIO.output(TRIG, True)
            # Send pulse for 10us
            time.sleep(0.00001)
            GPIO.output(TRIG, False)            
            
            pulse_start = 0
            pulse_end = 0
            
            # Start timing so we know if we're hanging
            start = time.time()
            
            # Now we calculate the return pulse width manually
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()
                if (pulse_start - start) > WAIT_TIME:
                	return ERROR
                	
            # Start timing again
            start = time.time()
            
            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()
                if (pulse_end - start) > WAIT_TIME:
                	return ERROR
            
            return pulse_end - pulse_start
        
        except Exception as e:
            print e
            GPIO.cleanup()
            print "Create new object to use ultrasound"    
        
    def getDistance(self):
    	pulse_width = ERROR
    	
        while pulse_width < 0 or pulse_width > FAILURE:
        	pulse_width = self.sendPulse()

        return self.toUAVFrame(round(pulse_width*17150,2))
