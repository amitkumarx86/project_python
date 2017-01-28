import numpy as np
import cv2

# Create a black image
img = np.zeros((1024,1024,4), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
#cv2.line(img,(0,0),(511,511),(255,0,0),5)

#cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)

#cv2.circle(img,(447,63), 63, (0,0,255), -1)

#cv2.ellipse(img,(256,256),(100,50),0,0,360,255,1)

#pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
#pts = pts.reshape((-1,1,2))
#cv2.polylines(img,[pts],True,(0,255,255))

font = cv2.FONT_HERSHEY_SIMPLEX
#cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2)

cv2.ellipse(img,(56,356),(50,100),0,0,360,255,1)
cv2.line(img,(120,300),(120,500),(255,0,0),1)
cv2.ellipse(img,(170,370),(50,70),0,0,360,255,1)
cv2.ellipse(img,(300,365),(70,65),0,0,300,255,1)
cv2.line(img,(260,310),(340,310),(255,0,0),1)
cv2.line(img,(380,300),(380,430),(255,0,0),1)
cv2.line(img,(450,300),(450,430),(255,0,0),1)
cv2.line(img,(380,315),(450,300),(255,0,0),1)
cv2.ellipse(img,(550,365),(70,65),0,0,300,255,1)

cv2.line(img,(750,300),(710,430),(255,0,0),1)
cv2.line(img,(630,300),(710,430),(255,0,0),1)

cv2.imshow('as',img)
cv2.waitKey(0)
cv2.destroyAllWindows()