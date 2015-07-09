# Servo Control
import time
        
class ServoControl:
	
	def __init__(self, id):
		self.id = id
		
	def setPosition(pos):
		pass

# class ServoControl:
# 
        # def __init__(self, delay):
                # self._delay = delay
                # self.servoControl = open(SERVO_PIPE,'w')
                # self.setAngle(self._minAngle)
# 
        # # Moves the servo from minAngle to maxAngle in small increments
        # def up(self):
                # # Initialise servo
                # angle = self._minAngle
                # self.setAngle(angle)
# 
                # angleIncrement = map(self._minWidth + self._increment, self._minWidth, self._maxWidth, self._minAngle, self._maxAngle) - self._minAngle
                # 
                # while angle < self._maxAngle:
                        # angle += angleIncrement
                        # self.setAngle(int(angle))
                        # time.sleep(self._delay)
# 
        # # Moves the servo from maxAngle to minAngle in small increments
        # def down(self):
                # # Initialise servo
                # angle = self._maxAngle
                # self.setAngle(angle)
# 
                # angleIncrement = map(self._minWidth + self._increment, self._minWidth, self._maxWidth, self._minAngle, self._maxAngle) - self._minAngle
                # 
                # while angle > self._minAngle:
                        # angle -= angleIncrement
                        # self.setAngle(int(angle))
                        # time.sleep(self._delay)
        # 
# 
        # # Tests movement from min to max value
        # def sweep(self):
                # for i in range(0,5):
                        # self.setAngle(180)
                        # time.sleep(self._delay)
# 
                        # self.setAngle(0)
                        # time.sleep(self._delay)
# 
        # def setAngle(self, angle):
                # value = map(angle, self._minAngle, self._maxAngle, self._minWidth, self._maxWidth)
                # print('Moving to ' + str(angle) + ' degrees\n')
                # self.servoControl.write('1=' + str(value) + 'us\n')
                # self.servoControl.flush()