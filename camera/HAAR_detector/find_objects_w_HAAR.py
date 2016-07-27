import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

#SAL
from saliency import Saliency
#HOG
#from imutils.object_detection import non_max_supression
#from imutils import paths
#import imutils


BUFFER = 40

#read an image
img_original = cv2.imread('test_image.jpg')
img_grayscale = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

img_sized = cv2.resize(img_original,(1280,720))
img_size_exclusion = img_sized.copy()
img_hist = img_sized.copy()
img_hog = img_sized.copy()

start = time.time()
#find the saliency map
sal = Saliency(img_sized)
sal_map = sal.get_saliency_map()

end = time.time()

test_duration = end-start

#convert to the correct type
sal_conv = (sal_map*255).round().astype(np.uint8)

#find the contours
ret,thresh = cv2.threshold(sal_conv,100,255,0)
_, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


font = cv2.FONT_HERSHEY_SIMPLEX
mask = np.zeros(img_sized.shape,np.uint8)
color = ('b','r','g')
object_detected = None
detection_queue = []

for cnt in contours:
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)+ BUFFER
    area = 3.141*(radius**2)
    
    print "Object Detected :: AREA - ", area
    
    if area >= 30000 and area <= 40000:
        print "IN RANGE AREA DETECTED"
        cv2.circle(img_size_exclusion,center,radius,(0,255,255),2)
        cv2.putText(img_size_exclusion,str(area),center,font,1,(255,255,255),2,cv2.LINE_AA)
        cv2.drawContours(mask,[cnt],0,255,-1)

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img_sized, [box],0,(0,0,255),2)
        x,y,w,h = cv2.boundingRect(cnt)
        h = h + BUFFER
        w = w + BUFFER
        object_detected = img_hist[y:y+h,x:x+w]

        #use a blank section to contrast against
        #y = y
        #y = x - 100
        #blank_example = img_hist[y:y+h,x:x+w]
        #place into the detection queue to be multiprocessed
        #need to make sure that we are taking the minimumn pixels for
        #required by the HOG detector
        a = 400 - h
        b = 400 - w
        print "a::" , a
        print "b::" , b
        if a > 0:
            y = int(y - 0.5*a)
            print "y::", y
            h = 400
            print "h::", h
        if b > 0:
            x = int(x - 0.5*b)
            w = 400
        
        if h < 400: h = 400
        if w < 400: w = 400
        
        hog_buffer = img_hist[y:y+h,x:x+w]
        haar_buffer = img_hist[y:y+h,x:x+w]
        detection_queue.insert(0,hog_buffer)
        
       
        
    cv2.circle(img_sized,center,radius,(0,255,0),2)
    cv2.putText(img_sized,str(area),center,font,1,(255,255,255),2,cv2.LINE_AA)

#iterate through the detected objects queue

#hog = cv2.HOGDescriptor()
#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

haar = cv2.CascadeClassifier(cv2.CascadeClassifier_getDefaultPeopleDetector())

count = 1

while detection_queue:
    score = 0
    object_query = detection_queue.pop()
    obj = object_query.copy()
    print "ANALYSING OBJECT ", count
    print "OBJECT SHAPE :: ", object_query.shape
    print " >> RUNNING HOG"
    #(rects, weights) = hog.detectMultiScale(object_query, winStride=(4,4),
    #                                            padding=(8,8), scale=1.05)
    #
    for (x,y,w,h) in rects:
        cv2.rectangle(hog_buffer, (x,y),(x+w,y+h),(0,0,255),2)
        print "   +HOG POS"
    print "OBJECT ", count, " SCORE :: ", score
    count = count + 1




#figure 1
fig = plt.figure(1)
fig.suptitle("Detection Time: " + str(test_duration))
#image 1
sub1 = plt.subplot(211)
sub1.set_title("Original Image")
plt.imshow(cv2.cvtColor(img_sized,cv2.COLOR_BGR2RGB))
#image 2
sub2 = plt.subplot(212)
sub2.set_title("Size Exclusion")
plt.imshow(cv2.cvtColor(img_size_exclusion,cv2.COLOR_BGR2RGB))

# figure 2
plt.figure(2)

#image 3
sub1 = plt.subplot(221)
sub1.set_title("Detected Object")
plt.imshow(cv2.cvtColor(object_detected,cv2.COLOR_BGR2RGB))

#image 4
sub2 = plt.subplot(222)
sub2.set_title("Negative Control")
#plt.imshow(cv2.cvtColor(blank_example,cv2.COLOR_BGR2RGB))

#image 5
plt.subplot(223)
for i,col in enumerate(color):
            #hist = cv2.calcHist([object_detected],[i],None,[256],[0,256])
            #plt.plot(hist,color=col)
    pass

#image 6
plt.subplot(224)
for i,col in enumerate(color):
            #hist = cv2.calcHist([blank_example],[i],None,[256],[0,256])
            #plt.plot(hist,color=col)
    pass

            
#plt.show()
            
cv2.imshow('image',hog_buffer)
cv2.waitKey(0)
cv2.destroyAllWindows
