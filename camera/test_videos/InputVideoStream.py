# import the necessary packages
from threading import Thread
from multiprocessing import Process
import cv2
 
class InputVideoStream:
    def __init__(self, src=0):
	# initialize the video camera stream and read the first frame
	# from the stream
	self.stream = cv2.VideoCapture(src)
	(self.grabbed, self.frame) = self.stream.read()
 
	# initialize the variable used to indicate if the thread should
	# be stopped
	self.stopped = False

    def start(self):
        #start the thread to read from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        #keep looping indefinately until the thread is stopped
        while True:
            #if the thread stop indicator is working then stop the thread
            if self.stopped:
                return

            #otherwise get the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        #return the most recently read
        return self.frame

    def stop(self):
        #indicate that the thread should be stopped
        self.stopped = True
