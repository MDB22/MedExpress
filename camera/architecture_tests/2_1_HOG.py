# Option 2.1
# this code examines the use of the singular hog detector
# as per the report option 2.1

from hog_classifier import HOGClassifier
import cv2
import time
import imutils

#video capture set up
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('outputs/output_hog_'+str(time.time())+'.avi',fourcc, 20.0, (720,480))
stream = cv2.VideoCapture('test.avi')

#image capture
image = cv2.imread('test_image.jpg', 1)
image = cv2.resize(image, (720,480))

# set up the HOG classifier
hog = HOGClassifier()

# detect from image test
(rects, weights) = hog.detect(image)
    
for (x,y,w,h) in rects:
  cv2.rectangle(image, (x,y),(x+w,y+h),(0,0,255),2)
  print "!PING!"

cv2.imwrite('images/image'+str(time.time())+'.jpg', image)

frames = 0

# loop over some frames

'''
while (stream.isOpened()):

  (flag, frame) = stream.read()
  
  if flag:
    frame = cv2.resize(frame, (720,480))
    (rects, weights) = hog.detect(frame)
    
    for (x,y,w,h) in rects:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        print "!PING!"
        
    out.write(frame)
    print "Written Frames:: ", frames
    frames = frames + 1
  else:
     break
	 
out.release()
stream.release()
cv2.destroyAllWindows()

 #out.write(frame)
            #cv2.imshow("Frame", frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
'''
