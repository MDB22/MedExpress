# Servo Control
import time

# Linear map from desired angle to control value
def map(value, range1_low, range1_high, range2_low, range2_high):
        # Convert the initial value into a 0-1 range (float)
        valueScaled = (value - range1_low) / float(range1_high - range1_low)

        # Convert the 0-1 range into a value in the new range.
        return range2_low + valueScaled * (range2_high - range2_low)

class Lidar:
        _minWidth = 620
        _maxWidth = 2500
        
        _minAngle = 0
        _maxAngle = 180

        # servoValue increment
        _increment = 2

        def __init__(self, delay):
                self._delay = delay
                self.servoControl = open('/dev/servoblaster','w')
                self.setAngle(self._minAngle)

        # Moves the servo from minAngle to maxAngle in small increments
        def up(self):
                # Initialise servo
                angle = self._minAngle
                self.setAngle(angle)

                angleIncrement = map(self._minWidth + self._increment, self._minWidth, self._maxWidth, self._minAngle, self._maxAngle) - self._minAngle
                
                while angle < self._maxAngle:
                        angle += angleIncrement
                        self.setAngle(int(angle))
                        time.sleep(self._delay)

        # Moves the servo from maxAngle to minAngle in small increments
        def down(self):
                # Initialise servo
                angle = self._maxAngle
                self.setAngle(angle)

                angleIncrement = map(self._minWidth + self._increment, self._minWidth, self._maxWidth, self._minAngle, self._maxAngle) - self._minAngle
                
                while angle > self._minAngle:
                        angle -= angleIncrement
                        self.setAngle(int(angle))
                        time.sleep(self._delay)
        

        # Tests movement from min to max value
        def sweep(self):
                for i in range(0,5):
                        self.setAngle(180)
                        time.sleep(self._delay)

                        self.setAngle(0)
                        time.sleep(self._delay)

        def setAngle(self, angle):
                value = map(angle, self._minAngle, self._maxAngle, self._minWidth, self._maxWidth)
                print('Moving to ' + str(angle) + ' degrees\n')
                self.servoControl.write('0=' + str(value) + 'us\n')
                self.servoControl.flush()
  
##def set(property, value):
##	try:
##		f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
##		f.write(value)
##		f.close()	
##	except:
##		print("Error writing to: " + property + " value: " + value)
## 
## 
##def setServo(angle):
##	set("servo", str(angle))
##	
##		
##set("delayed", "0")
##set("mode", "servo")
##set("servo_max", "180")
##set("active", "1")
## 
##delay_period = 0.01
## 
##while True:
##	for angle in range(0, 180):
##		setServo(angle)
##		time.sleep(delay_period)
##	for angle in range(0, 180):
##		setServo(180 - angle)
##		time.sleep(delay_period)
