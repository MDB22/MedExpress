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
		
	# Verify if provided image name has valid extension
	def __hasValidExtension__(self, filename):
		return True
	
	# Captures a single image from the camera
	def getImage(self):
		retval, image = self.camera.read()
		print retval
		
		# If retval is False, something has gone wrong, throw exception
		if retval is False:
			print 'Error'
			pass
		
		return image;
		
	# Writes the stored image to the given file location
	def writeImage(self, path, filename, image):
		# If there is no valid extension, can't write image
		if not self.__hasValidExtension__(filename):
			pass
		else:
			cv2.imwrite(filename, image)
			
	def showImage(self, windowName, image):
		cv2.imshow(windowName, image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			return