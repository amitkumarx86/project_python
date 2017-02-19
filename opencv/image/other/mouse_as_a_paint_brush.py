import cv2
import numpy as np

#events=[i for i in dir(cv2) if 'EVENT' in i ]
#print events

def draw_circle(event,x,y,flag,param):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		cv2.circle(img,(x,y),30	,(255,255,0),-1)


img=np.zeros((512,512,3),np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

# to quit the progrm
while (1):
	cv2.imshow('image',img)
	if cv2.waitKey(26) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows();

