import numpy as np
import cv2
from selenium import webdriver
import sys
import time



#  browser code 

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
driver.get("https://facebook.com")
username = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")
username.send_keys("<your email id>")
password.send_keys("<your password>")
driver.find_element_by_id("u_0_r").submit()


def nothing():
    pass
cap=cv2.VideoCapture(0)
minH=0
minS=58
minV=75
maxH=50
maxS=173
maxV=200
kernel = np.ones((5,5), np.uint8)

# cv2.namedWindow('image')
# cv2.createTrackbar('minH', 'image', minH, 180, nothing)
# cv2.createTrackbar('minS', 'image', minS, 180, nothing)
# cv2.createTrackbar('minV', 'image', minV, 180, nothing)
# cv2.createTrackbar('maxH', 'image', maxH, 180, nothing)
# cv2.createTrackbar('maxS', 'image', maxS, 255, nothing)
# cv2.createTrackbar('maxV', 'image', maxV, 255, nothing)

file = open("break.flag","r")
flag = file.read()
addList = []
i=0
end = 708
while(flag == "1"):
    #Capture frame by frame
    ret, frame=cap.read()
    frame = cv2.flip(frame,1) 
    #Convert to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #determine the range of hsv for skin color segementation
    lower_range=np.array([minH, minS, minV])
    higher_range=np.array([maxH, maxS, maxV])

    #masking th eimage according to the given range
    mask=cv2.inRange(hsv, lower_range, higher_range)

    #applying median blur
    median=cv2.medianBlur(mask, 5)

    #applying dilation
    dilate=cv2.dilate(median, kernel, iterations=1)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    #Displaying the resultig frame
    # cv2.imshow('frame', hsv)
    # cv2.imshow('image', mask)
    # cv2.imshow('blurred image', median)

    # find max contour in the image

    image, contours, hierarchy = cv2.findContours(dilate.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if(len(contours) == 0): continue

    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    a = sorted(contours, key = lambda x: cv2.contourArea(x) , reverse=True)
    print a
    # print cnt
    # hull = cv2.convexHull(cnt)
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    # print(cx, cy)
    addList.append([cx,cy])
    if(len(addList) > 10):
        x1 = addList[0][0]
        y1 = addList[0][1]
        x2 = addList[len(addList)-1][0]
        y2 = addList[len(addList)-1][1]
        # print y2-y1
        if((y2-y1) > 60):
            print "Scroll Down"
            driver.execute_script("window.scrollTo("+str(i)+", "+str(end)+");")
            i = end
            end = end + 708
            time.sleep(2)
        # elif((y2-y1) < -60):
        #     print "Scroll Up"
        #     driver.execute_script("window.scrollTo("+str(end)+", "+str(i)+");")
        #     end = i
        #     i = i - 708
        #     time.sleep(2)

        # print "last x = "+str(addList[len(addList)-1][0])
        # print "First y = "+str(addList[0][1])
        # print "last y = "+str(addList[len(addList)-1][1])
        
        addList[:] = []


    # cx = np.mean(hull.points[hull.vertices,0])
    # cy = np.mean(hull.points[hull.vertices,1])
    cv2.circle(frame,(cx,cy), 63, (0,0,255), -1)    
    # drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(frame, [cnt], 0, (0,255,0), 3)
    # cv2.drawContours(frame, [hull], 0,(0,255,0), 3)

    cv2.imshow('result',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    file = open("break.flag","r")
    flag = file.read()
#When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
   