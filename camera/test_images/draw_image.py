import cv2
import numpy as np

from matplotlib import pyplot as plt

#read an image
img = cv2.imread('test_image.jpg')

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV',(10,500), font,4,(0,0,0),2,cv2.LINE_AA)

plt.imshow(img, cmap='gray',interpolation='bicubic')
plt.xticks([]), plt.yticks([])
plt.show()
