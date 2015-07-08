import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

try: 
	print "Set up 1"
	GPIO.setup(TRIG, GPIO.OUT)
	print "Set up 2"
	GPIO.setup(ECHO, GPIO.IN)
	print "Set up 3"
	GPIO.output(TRIG, False)
	print "Waiting for sensor to settle"
	time.sleep(2)

except:
	GPIO.cleanup()

while True:
	try:
		print "Distance Measurement In Progress"
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		
		while GPIO.input(ECHO) == 0:
			pulse_start = time.time()
			
		while GPIO.input(ECHO) == 1:
			pulse_end = time.time()
			
		pulse_duration = pulse_end - pulse_start
		
		distance = pulse_duration * 17150
		
		distance = round(distance, 2)
		
		print "Distance:", distance, "cm"
		
	except Exception as e:
		print e
		GPIO.cleanup()
		break