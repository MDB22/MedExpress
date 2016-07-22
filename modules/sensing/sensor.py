# Abstract class to represent the sensors available to the system

class Sensor(object):

	state = {}

	def __init__(self, vehicle):
		self.vehicle = vehicle

	# Performs the "data acquisition" process for the sensor
	# Returns a dictionary where the key is the name of the sensor, 
	# and the value is the sensor measurement
	def getData(self):
		raise NotImplementedError("This method has not been implemented.")