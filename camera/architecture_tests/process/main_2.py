from multiprocessing import Process, Queue, Lock
import time as time
import numpy as np
import cv2 as cv2

def import_image(frame_queue, queue_lock):
  
  stream = cv2.VideoCapture('test.avi')
  timeOut = 0

  while timeOut < 500:
    (ret, frame) = stream.read()

    if ret:
      timeOut = 0
      frame = cv2.resize(frame, (1280,720))
      with queue_lock:
        if not frame_queue.full():
          frame_queue.put(frame)
        else:
          print "waiting for frame queue"
      print "frame"
  
  print "import timeout"


frame_queue = Queue()
queue_lock = Lock()

proc = Process(target=import_image, args=(frame_queue, queue_lock))

proc.start()
time.sleep(1)

timeOut = 0
while True:
  if frame_queue.empty():
    timeOut = timeOut + 1
  else:
    timeOut = 0
  if timeOut > 50:
    print "main timout"
    break

  

proc.terminate()
print "proc's terminated"
