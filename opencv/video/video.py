import numpy as np
import cv2
import myopencv as am

cap = cv2.VideoCapture(0)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	
	# Our operations on the frame come here
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# flip video
	if ret : 
		img = cv2.flip(frame,1)
		smoothImage = am.convertToGray(img)
		# smoothImage = am.adjustGamma(smoothImage,0.8)
		smoothImage = am.smoothenImage(smoothImage,5)
		thresh1 = am.globalThreshold(smoothImage,100)
		

		
		
		edges = am.canny(thresh1,10,100)
		

		# cv2.imshow('frame',edges)

		contours, hierarchy = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted(contours, key=cv2.contourArea, reverse=True)
		cv2.drawContours(img,contours,-1,(0,255,0),1)
		# cv2.imshow('frame',edges)
		cv2.imshow('frame',img)
		
		if(len(contours) < 0):
			cnt = contours[0]
				

			hull = cv2.convexHull(cnt,returnPoints = False)
			defects = cv2.convexityDefects(cnt,hull)
			if(len(defects) > 0):
				for i in range(defects.shape[0]):
					s,e,f,d = defects[i,0]
					start = tuple(cnt[s][0])
					end = tuple(cnt[e][0])
					far = tuple(cnt[f][0])
					cv2.line(img,start,end,[0,255,0],2)                
					cv2.circle(img,far,5,[0,0,255],-1)
					


				#cv2.drawContours(img,[hull],0,(0,255,0),2)
				


				# x,y,w,h = cv2.boundingRect(cnt)
				# cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
				
				
				# Display the resulting frame
				#edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),10,100)
				#contours, hierarchy = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				#cv2.drawContours(img, contours, -1, (0,255,0), 1)
				

				cv2.imshow('frame',img)
		
	else:
		print "failed to fetch video"
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
