import numpy as np
import cv2

img = cv2.imread('a.jpeg',0)
#res = cv2.resize(img,None, fx=.5, fy=.5, 	interpolation=cv2.INTER_CUBIC)
rows,cols = img.shape
M=np.float32([[1,0,100],[0,1,50]])
dst=cv2.warpAffine(img,M,(cols,rows))
cv2.imshow('img',dst);

cv2.waitKey(0)