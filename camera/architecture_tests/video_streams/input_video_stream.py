import cv2
import time
from multiprocessing import Process
from threading import Thread
class InputVideoStream:

  def __init__(self, src):
    # initilize the sream and read the first frame
    self.stream = cv2.VideoCapture(src)
    (self.grabbed, self.frame) = self.stream.read()
    self.stopped= False
    self.frames = 0
    self.p = Process(target=self.update, args=())

  def start(self):
    self.p.start()
    return self

  def update(self):
    print "update called"
    while True:
      (self.grabbed, self.frame) = self.stream.read()
      self.frames = self.frames + 1
      #print self.grabbed, " -> ", self.frames
      print "stream read"
      if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    #self.grabbed = False;
    print "update ended"
      
  def read(self):
    return (self.grabbed, self.frame)

  def stop(self):
    print "Thread Stopped!"
    self.p.terminate()
    self.stream.release()
    self.stopped = True

  def isGrabbed(self):
    return self.grabbed
