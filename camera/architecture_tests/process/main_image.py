# need to start multiple processes than then end up coming back together
# one process to bring in the frames and then
# one process to sort out the salinity

from multiprocessing import Process, Queue, Lock

import cv2
import time
import numpy as np
from saliency import Saliency

# this is where the processes are created
def sal_image(frame_queue, sal_queue, queue_lock):
  print "sal_image called"
  while True:
    if not frame_queue.empty():
        print "queue is not empty"
        
        queue_lock.acquire()
        img = frame_queue.get()
        queue_lock.release()
        
        sal = Saliency(img)
        sal_map = sal.get_saliency_map()
        sal_img = (sal_map*255).round().astype(np.uint8)
        img = cv2.cvtColor(sal_img, cv2.COLOR_GRAY2BGR)

        queue_lock.acquire()
        sal_queue.put(img)
        queue_lock.release()
        



def import_image(frame_queue, sal_queue, queue_lock):

  print "import_image called"
  
  #img = cv2.imread('test_image.jpg', 0)
  #img = cv2.resize(img, (1280,720))
  stream = cv2.VideoCapture('test.avi')

  while True:
    ret, frame = stream.read()
    frame = cv2.resize(frame, (1280, 720))
    if ret:
      time.sleep(1)
      queue_lock.acquire()
      frame_queue.put(frame)
      queue_lock.release()
    else:
      print "stream over"
      break
  
##  while True:
##    if not sal_queue.empty():
##      print "sal queue is not empty"
##      img = sal_queue.get()
##      cv2.imshow("img", img)
##      cv2.waitKey(0)
##      cv2.destroyAllWindows()
##      break

print "done"

queue_lock = Lock()
#this is the queue with the frames
frame_queue = Queue()
sal_queue = Queue()
#spin up the processes
p = Process(target=import_image, args=(frame_queue,sal_queue, queue_lock))
q = Process(target=sal_image, args=(frame_queue,sal_queue, queue_lock))

time.sleep(1)
p.start()
time.sleep(1)
q.start()

time.sleep(1)
i = 0

while True:
  time.sleep(1)
  if not sal_queue.empty():
    #frame = sal_queue.get()
    #cv2.imshow('frame', frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #  break
    print "processed frame"
  i = i + 1
  print "tick : ", i


p.join()
q.join()


##img = cv2.imread('test_image.jpg', 0)
##img = cv2.resize(img, (1280,720))
##
##frame_queue.put(img)
##
##i = 0
##while True:
##  if not sal_queue.empty():
##    print sal_queue.get()
####    img = sal_queue.get()
####    cv2.imshow("frame", img)
####    cv2.waitKey(0)
####    cv2.destroyAllWindows()
##    
##
##
####
##
####
####sal = Saliency(img)
####sal_map = sal.get_saliency_map()
####sal_img = (sal_map*255).round().astype(np.uint8)
####img = cv2.cvtColor(sal_img, cv2.COLOR_GRAY2BGR)
##
##print "done"
##
##time.sleep(1)



print "done"

