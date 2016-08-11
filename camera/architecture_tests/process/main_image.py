# need to start multiple processes than then end up coming back together
# one process to bring in the frames and then
# one process to sort out the salinity
# looks like the internal buffer could be overloading and then comeing to a deadlock
# the data pulled from the overannot fit in the buffer but the buffer never gets cleared because
# the process does not run


from multiprocessing import Process, Queue, Lock
import curses
import signal
import cv2
import time
import numpy as np
from saliency import Saliency

#textin = curses.initscr()
#textin.nodelay(1)

#def handler(signum, frame):
#  print 'you cannot terminate like this will stuff up the process'
# print 'please press j to join the process and then q to exit'

#ignal.signal(signal.SIGTSTP, handler)

# this is where the processes are created
def sal_image(frame_queue, sal_queue, queue_lock):
  print "sal_image called"
  frame = 0
  while True:
    if not frame_queue.empty():       
        queue_lock.acquire()
        img = frame_queue.get()
        queue_lock.release()
        
        sal = Saliency(img)
        sal_map = sal.get_saliency_map()
        sal_img = (sal_map*255).round().astype(np.uint8)
        img = cv2.cvtColor(sal_img, cv2.COLOR_GRAY2BGR)

        queue_lock.acquire()
        if sal_queue.qsize() < 3:
          sal_queue.put(img)
        else:
          time.sleep(1)
        queue_lock.release()
        frame = frame + 1
        print "SAL _ FRAME : ", frame
        



def import_image(frame_queue, sal_queue, queue_lock):

  print "import_image called"
  #img = cv2.imread('test_image.jpg',0)
  #img = cv2.resize(img, (1280,720)) 
  stream = cv2.VideoCapture('test.avi')
  i = 0

  ret, frame = stream.read()
  queue_lock.acquire()
  frame_queue.put(frame)
  queue_lock.release()
  while True:

    ret, frame = stream.read()
    #frame = img
    
    if ret:
      frame = cv2.resize(frame, (1280, 720))
      queue_lock.acquire()
      print frame_queue.qsize()
      if int(frame_queue.qsize) < 3:
        print "PUT TO FRAME"
        frame_queue.put(frame)
      else:
        time.sleep(1)
        
      queue_lock.release()
      i = i + 1
      print "INP _ FRAME, ", i
    else:
      print "stream over"
      break


print "done"



if __name__ == '__main__':
  queue_lock = Lock()
  frame_queue = Queue()
  sal_queue = Queue()


  p = Process(target=import_image, args=(frame_queue,sal_queue, queue_lock))
  q = Process(target=sal_image, args=(frame_queue,sal_queue, queue_lock))

  time.sleep(1)
  p.start()
  time.sleep(1)
  q.start()
  time.sleep(1)
  i = 0

  timeOut = 0

  while True:
  # need to have a timeout here

    if not sal_queue.empty():
      print "sal_queue not empty: ", sal_queue.qsize()
      timeOut = 0
      i = i +1
      frame = sal_queue.get()
      print "processed frame: ", i
    elif timeOut > 10:
      while not sal_queue.empty():
        trash = sal_queue.get()
      while not frame_queue.empty():
        transh = frame_queue.empty()
      print frame_queue.qsize()
      print sal_queue.qsize()
      p.terminate()
      q.terminate()
      print "main thread broken"
      break
    else:
      timeOut = timeOut + 1

      #print timeOut


  p.terminate()
  time.sleep(1)
  q.terminate()

  print "processes are joined"
  print "done"

