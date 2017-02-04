import numpy as np
import cv2

img = cv2.imread('a.jpeg')
res = cv2.resize(img,None, fx=.5, fy=.5, 	interpolation=cv2.INTER_CUBIC)
cv2.imshow('img',res);

cv2.waitKey(0)