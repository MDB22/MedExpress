# Option 2.2
# this code examines the use of the singular haar detector
# as per the report option 2.2

from haar_classifier import HAARClassifier
import cv2
import time

#video capture set up
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('outputs/output_haar_mix_'+str(time.time())+'.avi',fourcc, 20.0, (1280,720))
stream = cv2.VideoCapture('test.avi')

# set up the HAAR classifier
haar = HAARClassifier()

frames = 0

# loop over some frames
while (stream.isOpened()):

  (flag, frame) = stream.read()

  if flag:
    
    rects = haar.detectBodyFull(frame)
    for (x,y,w,h) in rects:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        print "!PING!"
        
    rects = haar.detectBodyUpper(frame)
    for (x,y,w,h) in rects:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        print "!PING!"
        
    rects = haar.detectBodyLower(frame)
    for (x,y,w,h) in rects:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
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
