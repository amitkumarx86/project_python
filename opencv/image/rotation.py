import numpy as np
import cv2

img = cv2.imread('a.jpeg',0)
#res = cv2.resize(img,None, fx=.5, fy=.5, 	interpolation=cv2.INTER_CUBIC)
rows,cols = img.shape
M=cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
dst=cv2.warpAffine(img,M,(cols,rows))
cv2.imshow('img',dst);

cv2.waitKey(0)