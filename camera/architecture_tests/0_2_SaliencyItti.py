# Option 2.2
# this code examines the use of the singular haar detector
# as per the report option 2.2
from fps import FPS
from saliency import Saliency
from video_streams import InputVideoStream
from multiprocessing import Queue, Lock
import numpy as np
import cv2
import time

# video capture set up
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('outputs/output_sal_proc_'+str(time.time())+'.avi',fourcc, 20.0, (1280,720))
# stream = cv2.VideoCapture('test.avi')

queue_lock = Lock()
frame_queue = Queue()

stream = InputVideoStream('test.avi', frame_queue, queue_lock)
time.sleep(1)
stream.start()

time.sleep(2)
frames = 0

# loop over some frames
fps = FPS()
fps.start()

while frames < 30:
  print "sal"
  with queue_lock:
    if not frame_queue.empty():
      print "PING"
      print "got lock"
      frame = frame_queue.get()
      sal = Saliency(frame)
      sal_map = sal.get_saliency_map()
    #sal_frame = (sal_map*255).round().astype(np.uint8)
    #frame = cv2.cvtColor(sal_frame, cv2.COLOR_GRAY2BGR)
    #out.write(frame)
      frames = frames + 1
      fps.update()
  
    else:
      break

fps.stop()
#out.release()
stream.join()
cv2.destroyAllWindows()


print "FPS :: ", fps.fps()
print "DUR :: ", fps.elapsed()
