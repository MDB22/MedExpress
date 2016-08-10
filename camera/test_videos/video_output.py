from InputVideoStream import InputVideoStream
from OutputVideoStream import OutputVideoStream

import time
from multiprocessing import Process, Queue
#from threading import Thread
from FPS import FPS
import imutils
import cv2
from saliency import Saliency
import numpy as np
import math

                        
framequeue = Queue()
outqueue = Queue()

output = OutputVideoStream(framequeue)
output.start()


#video capture set up
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('ouput.avi',fourcc, 20.0, (640,480))
#out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))




font = cv2.FONT_HERSHEY_SIMPLEX
# this is used to test the relative fps of the threaded and unthreaded options

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames without Threading...")
stream = cv2.VideoCapture('test.avi')

#proc = Process(target=frame_display, args=(taskqueue, outqueue))
#proc.start()

fps = FPS()
fps.start()
 
# loop over some frames
while fps._numFrames < 100:
	# grab the frame from the stream and resize it to have a maximum
	# width of 400 pixels
	(grabbed, frame) = stream.read()
	frame = cv2.resize(frame, (640,400))
        if grabbed:
                out.write(frame)
	#cv2.imshow("Frame", frame)
	#key = cv2.waitKey(1) & 0xFF

	fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: " + str(fps.elapsed()))
print("[INFO] approx. FPS:  " + str(fps.fps()))
 
# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = InputVideoStream('test.avi').start()
fps2 = FPS().start()
 
# loop over some frames...this time using the threaded stream
while fps2._numFrames < 100:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = cv2.resize(frame, (640,400))
 


        start = time.time()

        end = time.time()
        dur = end-start

       
	cv2.imshow("Frame", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
          break
 
	# update the FPS counter
	fps2.update()
 
# stop the timer and display FPS information
fps2.stop()
print("[INFO] elasped time: " + str(fps2.elapsed()))
print("[INFO] approx. FPS:  " + str(fps2.fps()))
 
# do a bit of cleanup

cv2.destroyAllWindows()
vs.stop()
output.stop()
out.release()
print "stream ended"

#send a message to the multiprocess to get them to stop 
#taskqueue.put(None)
#proc.join()
print "proc ended"
print "ended"

