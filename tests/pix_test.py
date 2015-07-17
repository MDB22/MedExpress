from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

# First get an instance of the API endpoint
api = local_connect()
# Get the connected vehicle (currently only one vehicle can be returned).
v = api.get_vehicles()[0]

# Get all vehicle attributes (state)
#print "\nGet all vehicle attribute values:"
#print " Location: %s" % v.location
#print " Attitude: %s" % v.attitude
#print " Velocity: %s" % v.velocity
#print " GPS: %s" % v.gps_0
#print " Groundspeed: %s" % v.groundspeed
#print " Airspeed: %s" % v.airspeed
#print " Mount status: %s" % v.mount_status
#print " Mode: %s" % v.mode.name    # settable
#print " Armed: %s" % v.armed    # settable

while(True):
    print v.attitude
