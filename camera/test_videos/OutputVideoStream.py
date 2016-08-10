# import the necessary packages
from threading import Thread
from multiprocessing import Process, Queue
import cv2
 
class OutputVideoStream:
    def __init__(self, queue):
	# initialize the video camera stream and read the first frame
	# from the stream
	self.queue = queue
	
	# initialize the variable used to indicate if the thread should
	# be stopped
	self.stopped = False

    def start(self):
        #start the thread to read from the video stream
        Process(target=self.update, args=()).start()
        return self

    def update(self):
        #keep looping indefinately until the thread is stopped
        while True:
            #if the thread stop indicator is working then stop the thread
            if self.stopped:
                return

            #otherwise get the next frame from the stream
            self.frame = self.queue.get()
            cv2.imshow('image',self.frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
              break

    def read(self):
        #return the most recently read
        return self.frame

    def stop(self):
        #indicate that the thread should be stopped
        self.stopped = True
        cv2.destroyAllWindows
