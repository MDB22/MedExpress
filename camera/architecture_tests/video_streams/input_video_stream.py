import cv2
import time
from multiprocessing import Process

class InputVideoStream(Process):

  def __init__(self, frame_queue, queue_lock):
    Process.__init__(self)
    self.stream = cv2.VideoCapture('test.avi')
    self.stopped = False
    self.queue_lock = queue_lock
    self.frame_queue = frame_queue

    ret, init_frame = self.stream.read()
    
    with self.queue_lock:
      self.frame_queue.put(init_frame)

  def run(self):
    while True:
      print self.frame_queue.qsize()
      with self.queue_lock:
        if self.frame_queue.qsize() < 5:
          ret, frame = self.stream.read()
          self.frame_queue.put(frame)
    print "Stream Closed"


