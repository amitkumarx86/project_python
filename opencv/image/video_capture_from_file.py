import numpy as np
import cv2

cap = cv2.VideoCapture('a.webm')

while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(gray,(184,0),(510,128),(255,0,0),3)
    cv2.imshow('frame',gray)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()