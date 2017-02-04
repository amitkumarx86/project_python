import numpy as np
import cv2
import myopencv as am

# loading cascade
haarcascade_upperbody = cv2.CascadeClassifier('cascades/haarcascade_upperbody.xml')
haarcascade_smile = cv2.CascadeClassifier('cascades/haarcascade_smile.xml')
haarcascade_russian_plate_number = cv2.CascadeClassifier('cascades/haarcascade_russian_plate_number.xml')
haarcascade_righteye_2splits = cv2.CascadeClassifier('cascades/haarcascade_righteye_2splits.xml')
haarcascade_profileface = cv2.CascadeClassifier('cascades/haarcascade_profileface.xml')
haarcascade_mcs_upperbody = cv2.CascadeClassifier('cascades/haarcascade_mcs_upperbody.xml')
haarcascade_mcs_righteye = cv2.CascadeClassifier('cascades/haarcascade_mcs_righteye.xml')
haarcascade_mcs_rightear = cv2.CascadeClassifier('cascades/haarcascade_mcs_rightear.xml')
haarcascade_mcs_nose = cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml')
haarcascade_mcs_mouth = cv2.CascadeClassifier('cascades/haarcascade_mcs_mouth.xml')
haarcascade_mcs_lefteye = cv2.CascadeClassifier('cascades/haarcascade_mcs_lefteye.xml')
haarcascade_mcs_leftear = cv2.CascadeClassifier('cascades/haarcascade_mcs_leftear.xml')
haarcascade_mcs_eyepair_small = cv2.CascadeClassifier('cascades/haarcascade_mcs_eyepair_small.xml')
haarcascade_mcs_eyepair_big = cv2.CascadeClassifier('cascades/haarcascade_mcs_eyepair_big.xml')
haarcascade_lowerbody = cv2.CascadeClassifier('cascades/haarcascade_lowerbody.xml')
haarcascade_licence_plate_rus_16stages = cv2.CascadeClassifier('cascades/haarcascade_licence_plate_rus_16stages.xml')
haarcascade_lefteye_2splits = cv2.CascadeClassifier('cascades/haarcascade_lefteye_2splits.xml')
haarcascade_fullbody = cv2.CascadeClassifier('cascades/haarcascade_fullbody.xml')
haarcascade_frontalface_default = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
haarcascade_frontalface_alt = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')
haarcascade_frontalface_alt_tree = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt_tree.xml')
haarcascade_frontalface_alt2 = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')
haarcascade_frontalcatface = cv2.CascadeClassifier('cascades/haarcascade_frontalcatface.xml')
haarcascade_frontalcatface_extended = cv2.CascadeClassifier('cascades/haarcascade_frontalcatface_extended.xml')
haarcascade_eye = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
haarcascade_eye_tree_eyeglasses = cv2.CascadeClassifier('cascades/haarcascade_eye_tree_eyeglasses.xml')



img = cv2.imread('a.jpg')
img = img.resize()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = haarcascade_lowerbody.detectMultiScale(gray)
for (x,y,w,h) in faces:
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow('img',img)

"""
cap = cv2.VideoCapture(0)
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	
	if ret : 
		# flip video
		img = cv2.flip(frame,1)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = haarcascade_frontalface_default.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		cv2.imshow('img',img)
	else:
		print "failed to fetch video"
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
"""
cv2.waitKey(0)
cv2.destroyAllWindows()
