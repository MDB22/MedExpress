import dronekit 
from dronekit import connect, VehicleMode
import picamera
import time
import datetime

print "Hello there"
connection_string = "tcp:"
print "Connecting to vehicle on: %s" %(connection_string)

vehicle = connect("127.0.0.1:14550", "baud=56700",wait_ready=True)
camera = picamera.PiCamera()


while vehicle.isarmable():
  while vehicle.armed():
    camera.start_recording("/home/pi/usbdrv/video"+str(time.time())+".h264")
    time.sleep(1)
  camera.stop_recording()


#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
#
  
