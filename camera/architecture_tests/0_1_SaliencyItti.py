# Option 2.2
# this code examines the use of the singular haar detector
# as per the report option 2.2
from fps import FPS
from saliency import Saliency
import numpy as np
import cv2
import time

###video capture set up
##fourcc = cv2.VideoWriter_fourcc(*'XVID')
##out = cv2.VideoWriter('outputs/output_sal_'+str(time.time())+'.avi',fourcc, 20.0, (1280,720))
stream = cv2.VideoCapture('test.avi')
frames = 0

fps = FPS()

# start the FPS calculator
fps.start()
# loop over some frames
while (stream.isOpened()):

  (flag, frame) = stream.read()
  print flag
  #print "FLAG", flag
  if flag:
    
    sal = Saliency(frame)
    sal_map = sal.get_saliency_map()
    sal_frame = (sal_map*255).round().astype(np.uint8)
    frame = cv2.cvtColor(sal_frame, cv2.COLOR_GRAY2BGR)

##    out.write(frame)

    frames = frames + 1
    fps.update()
    
  else:
     break

fps.stop()
##out.release()
stream.release()
cv2.destroyAllWindows()
print "FPS :: ", fps.fps()
print "DUR :: ", fps.elapsed()

