import cv2




#video capture set up
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
#out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))

stream = cv2.VideoCapture('test.avi')

 
# loop over some frames
while (stream.isOpened()):
	# grab the frame from the stream and resize it to have a maximum
	# width of 400 pixels
	(grabbed, frame) = stream.read()
	
	
        if grabbed:
                
                frame = cv2.resize(frame, (640,480))
                out.write(frame)
                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break
	
 

 
out.release()
stream.release()
cv2.destroyAllWindows()


