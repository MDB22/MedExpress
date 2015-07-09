import cv2
import numpy as np

class Camera():
    
    # USB Port for camera, -1 if only a single camera
    CAMERA_PORT = -1
    
    def __init__(self, refreshRate):
        # VideoCapture object to retrieve images from webcam
        self.camera = cv2.VideoCapture(self.CAMERA_PORT)
        
        # Desired update frequency for object (in Hz)
        self.refreshRate = refreshRate 
        
    # Cleanup operations
    def __del__(self):
        self.camera.release()
            
    # Captures a single image from the camera
    def getImage(self):
        retval, image = self.camera.read()
        print retval
        
        # If retval is False, something has gone wrong, throw exception
        if retval is False:
            print 'Error'
            # Exception here
        
        return image;
        
    # Writes the stored image to the given file location
    def writeImage(self, path, filename, image):
        retval = self.camera.grab()
        print retval
        retval, image = self.camera.retrieve()
        print retval
        
        print cv2.imwrite(path + filename, image)
            
    def showImage(self, windowName, image):
        cv2.imshow(windowName, image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return