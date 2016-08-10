import cv2
import time
import numpy as np

class HOGClassifier:

  def __init__(self):
    self.classifier = cv2.HOGDescriptor()
    self.classifier.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    print "HOG CLASSIFIER DEFINED - DEFAULT PEOPLE"

  def detect(self, frame):
    (rects, weights) = self.classifier.detectMultiScale(frame,
                        winStride=(4,4), padding=(8,8), scale=1.05)
    print "HOG CLASSIFIER DETECT RETURN"
    return (rects, weights)                

  def run_scale_bench(self, frame):
    start_scale = 1.01
    end_scale = 1.10
    increment = 0.005

    test_values = np.arange(start_scale, end_scale, increment)
    
    for test_scale in test_values:
      start = time.time()
      (rects, weights) = self.classifier.detectMultiScale(frame,
                          winStride=(4,4), padding=(8,8), scale=test_scale)
      end = time.time()
      print "TEST ", test_scale, " DUR -- ",  (end - start), " D -> ", len(rects)
    print "HOG CLASSIFIER SCALE TEST FINISHED"



  
  
