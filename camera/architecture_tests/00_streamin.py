from video_streams import InputVideoStream
from multiprocessing import Lock, Queue
import cv2 as cv2
import numpy as np
import time as time


queue_lock = Lock()
frame_queue = Queue()


proc = InputVideoStream(frame_queue, queue_lock)

proc.start()

timeout = 0
start = time.time()

while timeout < 5:
  frame = frame_queue.get()
  #print frame_queue.qsize()
  end = time.time()
  timeout = end - start
  
print " [END!] main thread has timed out"
while not frame_queue.empty():
  print "pull -- ", frame_queue.qsize()
  img = frame_queue.get()
proc.terminate()



