from multiprocessing import Process, Queue, Lock
import time as time
import numpy as np
import cv2 as cv2
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('output_sal_proc_'+str(time.time())+'.avi',fourcc, 20.0, (1280,720))

def import_image(frame_queue, queue_lock):
  
  stream = cv2.VideoCapture('test.avi')
  timeOut = 0

  frames = 0
  
  while timeOut < 500:
    (ret, frame) = stream.read()

    if ret:
      timeOut = 0
      frame = cv2.resize(frame, (1280,720))
      with queue_lock:
        if frame_queue.qsize() < 3:
          frame_queue.put(frame)
          frames = frames + 1
        else:
          print "waiting for frame queue"
      print "frame", frames
  
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
    with queue_lock:
      img = frame_queue.get()
      output.write(img)
  if timeOut > 50000:
    print "main timout"
    break

  

proc.terminate()
output.release()
print "proc's terminated"
