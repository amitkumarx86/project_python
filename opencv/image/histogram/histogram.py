import cv2
from  matplotlib import pyplot as plt
import numpy as np

img = cv2.imread('a.jpg')

hist=cv2.calcHist([img],[0],None,[256],[0,256])
mask=np.zeros(img.shape[:2],np.uint8)
mask[200:300,100:400] = 255

masked_img = cv2.bitwise_and(img,img,mask=mask)
masked_hist=cv2.calcHist([masked_img],[0],None,[256],[0,256])

plt.subplot(221), plt.imshow(img)
plt.xticks([1,2,3]),plt.yticks([])

plt.subplot(222), plt.imshow(masked_img)
plt.subplot(223), plt.plot(hist), plt.plot(masked_hist)

plt.xlim([0,256])

plt.show()
