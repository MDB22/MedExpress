# Option 2.2
# this code examines the use of the singular haar detector
# as per the report option 2.2

from saliency import Saliency
from video_streams import InputVideoStream
import numpy as np
import cv2
import time

#video capture set up
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('outputs/output'+str(time.time())+'.avi',fourcc, 20.0, (1280,720))
#stream = cv2.VideoCapture('test.avi')
stream = InputVideoStream('test.avi').start()
frames = 0

# loop over some frames
while (stream.isOpened()):

  (flag, frame) = stream.read()

  if flag:
    
    sal = Saliency(frame)
    sal_map = sal.get_saliency_map()
    sal_frame = (sal_map*255).round().astype(np.uint8)
    frame = cv2.cvtColor(sal_frame, cv2.COLOR_GRAY2BGR)
    #print sal_frame.shape
    #print sal_map.shape
    #print frame.shape

    out.write(frame)
    print "Written Frames:: ", frames
    frames = frames + 1
  else:
     break


out.release()
#stream.release()
stream.stop()
cv2.destroyAllWindows()

 #out.write(frame)
            #cv2.imshow("Frame", frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
