# Manages and retrieves sensor data from the Pixhawk's GPS
import sensor

class Position(sensor.Sensor):

	state = {'lat': 0, 'lon': 0, 'alt': 0}

	def __init__(self, vehicle):
		super(Position, self).__init__(vehicle)

		self.vehicle.add_attribute_listener('location.global_frame', __sensor_callback__)

	def getData(self):
		return Position.state

def __sensor_callback__(self, name, value):
	# GPS location, with altitude relative to MSL
	Position.state['lat'] = value.lat
	Position.state['lon'] = value.lon
	Position.state['alt'] = value.alt