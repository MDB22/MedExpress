# Option 2.2
# this code examines the use of the singular haar detector
# as per the report option 2.2
from fps import FPS
from saliency import Saliency
from saliency import MPSaliency
from video_streams import InputVideoStream
from multiprocessing import Queue, Lock, Process
import numpy as np
import cv2
import time

# video capture set up
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('outputs/output_sal_proc_'+str(time.time())+'.avi',fourcc, 20.0, (1280,720))
# stream = cv2.VideoCapture('test.avi')

def import_image(frame_queue, queue_lock):
  
  stream = cv2.VideoCapture('test.avi')
  timeOut = 0

  frames = 0
  
  while timeOut < 500:
    (ret, frame) = stream.read()

    if ret:
      timeOut = 0
      frame = cv2.resize(frame, (1280,720))
      #print frame_queue.qsize()
      with queue_lock:
        if frame_queue.qsize() < 3:
          frame_queue.put(frame)
          frames = frames + 1
          print "frame::", frames, ": Q - ", frame_queue.qsize()
        else:
          pass
          #print "waiting for frame queue"
  print "import timeout"


queue_lock = Lock()
frame_queue = Queue()

stream = Process(target=import_image, args=(frame_queue, queue_lock))
time.sleep(1)
stream.start()

frames = 0

# loop over some frames
fps = FPS()
fps.start()

timeOut = 0



while frames < 300:
  #print "Main Thread Queue - > ",frame_queue.qsize() 
  with queue_lock:
    if not frame_queue.empty():
      timeOut = 0
      frame = frame_queue.get()
      sal = MPSaliency(frame)
      sal_map = sal.get_saliency_map()
      #sal_frame = (sal_map*255).round().astype(np.uint8)
      #frame = cv2.cvtColor(sal_frame, cv2.COLOR_GRAY2BGR)
      #out.write(frame)
      frames = frames + 1
      fps.update()
    else:
        pass
  

fps.stop()
stream.terminate()
cv2.destroyAllWindows()
#out.release()

print "FPS :: ", fps.fps()
print "DUR :: ", fps.elapsed()
