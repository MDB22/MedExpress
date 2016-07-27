import cv2
import numpy as np
from saliency import Saliency
from matplotlib import pyplot as plt

#read an image
img_original = cv2.imread('test_image.jpg')
#img_sized = cv2.resize(img_original,(1920,1080))
img_sized = cv2.resize(img_original,(1280,720))

sal = Saliency(img_sized)
sal_map = sal.get_saliency_map()

#figure 1
plt.figure(1)
#image 1
plt.subplot(211)
plt.imshow(img_sized)
#image 2
plt.subplot(212)
plt.imshow(sal_map)

plt.show()
