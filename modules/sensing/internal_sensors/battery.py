# Manages and retrieves sensor data from the Pixhawk's battery sensors
import sensor

class Battery(sensor.Sensor):

	state = {'voltage': 0, 'current': 0}

	def __init__(self, vehicle):
		super(Battery, self).__init__(vehicle)

		self.vehicle.add_attribute_listener('battery', __sensor_callback__)

	def getData(self):
		return Battery.state

def __sensor_callback__(self, name, value):
	Battery.state['voltage'] = self.battery.voltage
	Battery.state['current'] = self.battery.current