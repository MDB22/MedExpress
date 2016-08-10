import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import math
#SAL
from saliency import Saliency
#HOG
#from imutils.object_detection import non_max_supression
#from imutils import paths
#import imutils


def get_distance_from_pixel(image_shape, pixel_addr, altitude):
    # this method takes in an image altitude, and address and
    # attempts to determine the straight line distance and ground distance and
    # heading adjustments for use in the GPS coordinates function
    # from a drone to an object

    #unpack the inputs
    img_px_h = image_shape[0]
    img_px_w = image_shape[1]
    px_addr_v = pixel_addr[1]
    px_addr_h = pixel_addr[0]

    #determine the verticle angle
    px_fraction_v = float(px_addr_v)/float(img_px_h)
    angle_v = (10 + 40 * (px_fraction_v))*(math.pi/180) # DEAL WITH THE MAGIC NUMBERS
    dist_v = altitude/math.sin(angle_v)

    #determine the horizontal angle
    center_to_edge = dist_v*math.tan(25.6*(math.pi/180))
    #readdress the horizontal pixel from he center
    c_px_addr_w = int(px_addr_h - (img_px_w/2))
    abs_hor_dist = math.fabs(c_px_addr_w)
    hor_dist_fraction = float(abs_hor_dist)/(float(img_px_w)/2)
    hor_dist_fraction_signed = float(c_px_addr_w)/(float(img_px_w)/2)
    #find the distance from center out
    #from the ratio of the total distance 
    dist_from_center = center_to_edge*hor_dist_fraction
    # the angle from the heading
    target_bearing = hor_dist_fraction_signed * 26.5 #magic number from raspi camera fov

    # straight line distance
    sl_distance = math.sqrt(dist_from_center**2 + dist_v**2)
    # ground distance
    gn_distance = math.sqrt(sl_distance**2 - altitude**2)
    
    return (target_bearing, gn_distance, sl_distance)

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
    
    #print "Object Detected :: AREA - ", area
    
    if area >= 30000 and area <= 40000:
        #print "IN RANGE AREA DETECTED"
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
        #print "a::" , a
        #print "b::" , b
        if a > 0:
            y = int(y - 0.5*a)
            h = 400
        if b > 0:
            x = int(x - 0.5*b)
            w = 400
        
        if h < 400: h = 400
        if w < 400: w = 400
        
        hog_buffer = img_hist[y:y+h,x:x+w]
        haar_buffer = img_hist[y:y+h,x:x+w]
        detection_queue.insert(0,hog_buffer)
        cv2.putText(img_sized,str(center),center,font,1,(0,255,255),2,cv2.LINE_AA)
        #print "horizontal :: ", center[1]
        #print "verticle :: ", center[0]
    
        # hacky implementation of the distance function
        altitude = 10
        print "METHOD RETURN:->", get_distance_from_pixel(img_sized.shape, center, altitude)
        
        #alititude = 10# meters
        v_pixels = center[0]
        v_pixels_tot = img_sized.shape[0]
        print v_pixels
        print v_pixels_tot
        v_pixel_fraction = float(v_pixels) / float(v_pixels_tot)
        angle = (10 + 40*(v_pixel_fraction))*(math.pi/180)

        verticle_distance = altitude/math.sin(angle)
        #print "vert_distance::", verticle_distance

        from_center_width = verticle_distance*math.tan(25.6*(math.pi/180))
        dist_p_pixel = from_center_width/img_sized.shape[1]
        
        #distance from center
        #print img_sized.shape
        center_point = int(img_sized.shape[1]/2)
        dist_from_center = center[0] - center_point
        #print "center at:: ", center_point
        #print "distance_from_center::", dist_from_center
    cv2.circle(img_sized,center,radius,(0,255,0),2)
    cv2.putText(img_sized,str(area),center,font,1,(255,255,255),1,cv2.LINE_AA)
    

#iterate through the detected objects queue

#hog = cv2.HOGDescriptor()
#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

body_cascade = cv2.CascadeClassifier('haar_classifiers/haarcascade_fullbody.xml')
face_cascade = cv2.CascadeClassifier('haar_classifiers/haarcascade_frontalface_default.xml')
count = 1

while detection_queue:
    score = 0
    object_query = detection_queue.pop()
    obj = object_query.copy()
    #print "ANALYSING OBJECT ", count
    #print "OBJECT SHAPE :: ", object_query.shape
    #print " >> RUNNING HOG"
    #(rects, weights) = hog.detectMultiScale(object_query, winStride=(4,4),
    #                                            padding=(8,8), scale=1.05)
    #
    bodies = body_cascade.detectMultiScale(object_query, 1.3, 5)
    
    for (x, y, w, h) in bodies:
        roi = haar_buffer[y:y+h, x:x+w]
        cv2.rectangle(haar_buffer,(x,y),(x+w,y+h),(0,255,0),2)
        faces = face_cascade.detectMultiScale(roi, 1.3, 5)

        for (x, y, w, h) in faces:
            print "FACE"
            cv2.rectangle(haar_buffer,(x,y),(x+w,y+h), (255,0,0),2)   


    count = count + 1




#figure 1
fig = plt.figure(1)
fig.suptitle("Detection Time: " + str(test_duration))
#image 1
sub1 = plt.subplot(211)
sub1.set_title("Detection Image")
plt.imshow(cv2.cvtColor(img_sized,cv2.COLOR_BGR2RGB))
sub1 = plt.subplot(212)
sub1.set_title("Object")
plt.imshow(cv2.cvtColor(haar_buffer,cv2.COLOR_BGR2RGB))
plt.show()
            
#cv2.imshow('image',hog_buffer)
#cv2.waitKey(0)
#cv2.destroyAllWindows
