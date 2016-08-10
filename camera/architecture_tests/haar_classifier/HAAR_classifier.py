import cv2

bodyfull_path = '/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_fullbody.xml'
bodylower_path= '/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_lowerbody.xml'
bodyupper_path = '/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_upperbody.xml'

#detectMultiScale(IMAGE, SCALE_FACTOR, MINNEIGHBOURS, FLAGS, MINSIZE, MAXSIZE)
# SCALE FACTOR -    how much each image is scaled up or  down
# MINNEIGHBOURS -   how many boxes are required for there to be a detection
# FLAGS -           redundant from previous class
# MINSIZE -         the minimum size a component must be
# MAXSIZE -         the maximum size a component must be

class HAARClassifier:

  def __init__(self):
    self.fullbody = cv2.CascadeClassifier(bodyfull_path)
    self.upperbody = cv2.CascadeClassifier(bodyupper_path)
    self.lowerbody = cv2.CascadeClassifier(bodylower_path)
    print "HAAR CLASSIFIER - FULLBODY"

  def detectBodyFull(self, frame):
    PARAM_ONE = 1.3     # unknown param requires optimisation
    PARAM_TWO = 5       # unknown param requires optimisation
    rects = self.fullbody.detectMultiScale(frame, 1.3, 5)
    return rects

  def detectBodyUpper(self, frame):
    PARAM_ONE = 1.3     # unknown param requires optimisation
    PARAM_TWO = 5       # unknown param requires optimisation
    rects = self.upperbody.detectMultiScale(frame, 1.3, 5)
    return rects
  
  def detectBodyLower(self, frame):
    PARAM_ONE = 1.3     # unknown param requires optimisation
    PARAM_TWO = 5       # unknown param requires optimisation
    rects = self.lowerbody.detectMultiScale(frame, 1.3, 5)
    return rects
