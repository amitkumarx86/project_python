import cv2
import numpy as np
flags = [i for i in dir(cv2) if i.startswith('COLOR_BGR')]
print len(flags)

img=cv2.imread('c.jpeg')
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#cv2.imshow('image',img)

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_or(img,img, mask= mask)
cv2.imshow('frame',img)
cv2.imshow('mask',mask)
cv2.imshow('res',res)

cv2.waitKey(0)
cv2.destroyAllWindows()