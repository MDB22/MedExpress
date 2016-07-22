from sensing import *

import multiprocessing

class Sensors(multiprocessing.Process):

	def __init__(self, vehicle):
		super(Sensors, self).__init__()

		# Instantiate all sensors
		battery = Battery(vehicle)
		position = Position(vehicle)

		# Dictionary to record vehicle state attributes
		self.vehicle_state = {}

		# List of all sensors
		self.sensors = [battery, position]

	def run(self):
		for i in range(10):
			for sensor in self.sensors:
				self.vehicle_state.update(sensor.getData())
				
			print self.vehicle_state
			time.sleep(2)

		return