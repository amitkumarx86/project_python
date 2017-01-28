import numpy as np
import cv2

cap=cv2.VideoCapture(0)


#fourcc = cv2.VideoWriter_fourcc(*'XVID')  # this is used in open cv 3
fourcc = cv2.cv.CV_FOURCC(*'DIVX')
out=cv2.VideoWriter('output.avi',fourcc,20,(640,480),False)
# false for gray scale
while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			frame=cv2.flip(frame,1)
			out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
			cv2.imshow('frame',frame)
			if cv2.waitKey(26) & 0xFF == ord('q'):
				break
		else:
			break
cap.release()
out.release()
cv2.destroyAllWindows()