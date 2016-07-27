import cv2
import numpy as np

from matplotlib import pyplot as plt

#read an image
img = cv2.imread('test_image.jpg')

#write an image
#cv2.imwrite('saved_image.jpg',img)

# show with cv2 imshow function
#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows

# show with matplotlib
plt.imshow(img, cmap='gray',interpolation='bicubic')
plt.xticks([]), plt.yticks([])
plt.show()
