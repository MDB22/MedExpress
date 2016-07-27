import cv2
import numpy as np
from saliency import Saliency
from matplotlib import pyplot as plt
import time

BUFFER = 40

#read an image
img_original = cv2.imread('test_image.jpg')
img_grayscale = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
#img_sized = cv2.resize(img_original,(1920,1080))
img_sized = cv2.resize(img_original,(1280,720))
img_size_exclusion = img_sized.copy()
img_hist = img_sized.copy()

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

print len(contours)
#cnt = contours[0]
#print len(cnt)
#draw the contours on the original image
#cv2.drawContours(img_sized,contours,0,(0,0,0),3)

#for cnt in range(len(contours)):
#    x,y,w,h = cv2.boundingRect(cnt)
#    cv2.rectangle(img_sized,(x,y),(x+w,y+h),(0,255,0),2)

font = cv2.FONT_HERSHEY_SIMPLEX

mask = np.zeros(img_sized.shape,np.uint8)

color = ('b','r','g')

objectDetected = None

for cnt in contours:
#    rect = cv2.minAreaRect(cnt)
#    box = cv2.boxPoints(rect)
#    box = np.int0(box)
#    cv2.drawContours(img_sized, [box],0,(0,0,255),2)
#    x,y,w,h = cv2.boundingRect(cnt)
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)+ BUFFER
    area = 3.141*(radius**2)
    print area
    if area >= 30000 and area <= 40000:
        print "det correct area"
        print area
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
        objectDetected = img_hist[y:y+h,x:x+w]

        #offset
        y = y
        x = x - 100
        blankExample = img_hist[y:y+h,x:x+w]

        
            
        
    cv2.circle(img_sized,center,radius,(0,255,0),2)
    cv2.putText(img_sized,str(area),center,font,1,(255,255,255),2,cv2.LINE_AA)
#    x,y,w,h = cv2.boundingRect(cnt)
#    cv2.rectangle(img_sized,(x,y),(x+w,y+h),(0,255,0),2)
    

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
plt.imshow(cv2.cvtColor(objectDetected,cv2.COLOR_BGR2RGB))

#image 4
sub2 = plt.subplot(222)
sub2.set_title("Negative Control")
plt.imshow(cv2.cvtColor(blankExample,cv2.COLOR_BGR2RGB))

#image 5
plt.subplot(223)
for i,col in enumerate(color):
            hist = cv2.calcHist([objectDetected],[i],None,[256],[0,256])
            plt.plot(hist,color=col)

#image 6
plt.subplot(224)
for i,col in enumerate(color):
            hist = cv2.calcHist([blankExample],[i],None,[256],[0,256])
            plt.plot(hist,color=col)

            
plt.show()
#cv2.imshow('image',sal_map_int8)
#cv2.waitKey(0)
#cv2.destroyAllWindows
