# Class for interfacing with the ultrasonic sensor

import RPi.GPIO as GPIO
import time

# Pin associated with "triggering" the sensor
TRIG = 27
# Pin that returns data from sensor
ECHO = 22

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
        #time.sleep(2)
        print "Initialisation complete, ultrasound ready"

    def __del__(self):
        GPIO.cleanup()
        
    def getRange(self):
        try:
            # Trigger the ultrasound pulse
            GPIO.output(TRIG, True)
            # Send 10us pulse
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            
            # Now we calculate the return pulse width manually
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()
                
            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()
                
            pulse_duration = pulse_end - pulse_start
            
            distance = round(pulse_duration * 17150, 2)
            
            return distance
        
        except Exception as e:
            print e
            GPIO.cleanup()
            print "Create new object to use ultrasound"