from dronekit import *
from sensing import *

# Connect to simulated vehicle
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

# Instantiate all sensors
battery = Battery(vehicle)
position = Position(vehicle)

# Dictionary to record vehicle state attributes
vehicle_state = {}

# List of all sensors
sensors = [battery, position]

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

        
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True    

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print "Reached target altitude"
            break
        time.sleep(1)

    def printState():    	
		for i in range(10):
			for sensor in sensors:
				vehicle_state.update(sensor.getData())

			print vehicle_state
			time.sleep(1)

arm_and_takeoff(10)

print "Set default/target airspeed to 3"
vehicle.airspeed = 3

print "Going towards first point for 30 seconds ..."
point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
vehicle.simple_goto(point1)

# Test sensor acquisition
printState()

print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
vehicle.simple_goto(point2, groundspeed=10)

printState()

# sleep so we can see the change in map
time.sleep(30)

print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")

printState()

# Close vehicle object before exiting
vehicle.close()