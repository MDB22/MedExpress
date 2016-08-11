import cv2
import time
from multiprocessing import Process
from threading import Thread

class InputVideoStream(Process):

  def __init__(self, src, frame_queue, queue_lock):
    # initilize the sream and read the first frame
    Process.__init__(self)
    self.stream = cv2.VideoCapture(src)
    (self.grabbed, self.frame) = self.stream.read()
    self.stopped= False
    self.frames = 0
    self.frame_queue = frame_queue
    self.queue_lock = queue_lock

  def run(self):
    while True:
      (grabbed, frame) = self.stream.read()
      print "vid"
      if grabbed:
        self.frames = self.frames + 1
        with self.queue_lock:
          print "got lock"
          self.frame_queue.put(frame)


        print self.frames
      else:
        print "NF!"


