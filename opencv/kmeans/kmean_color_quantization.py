
import numpy as np
import cv2

"""
Color Quantization is the process of reducing number of colors in an image. 
One reason to do so is to reduce the memory. Sometimes, some devices may have limitation such that it can produce only 
limited number of colors. In those cases also, color quantization is performed. Here we use k-means clustering for color quantization.

There is nothing new to be explained here. There are 3 features, say, R,G,B. So we need to reshape the image to an array of
 Mx3 size (M is number of pixels in image). And after the clustering, 
 we apply centroid values (it is also R,G,B) to all pixels, such that resulting image will have 
 specified number of colors. And again we need to reshape it back to the shape of original image. Below is the code:
"""

img = cv2.imread('home.png')
Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8
ret,label,center=cv2.kmeans(Z,K,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

cv2.imshow('res2',res2)
cv2.waitKey(0)
cv2.destroyAllWindows()