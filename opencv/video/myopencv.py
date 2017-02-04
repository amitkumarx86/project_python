import numpy as np
import cv2
import sys # for command line arguments
import os # for listing files

def convertToGray(image):
	return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

def gaussianBlur(image,kernel):
	return cv2.GaussianBlur(image,(kernel,kernel),0)

def globalThreshold(image,thresholdValue):
	ret,th1 =  cv2.threshold(image,thresholdValue,255,cv2.THRESH_BINARY)
	return th1

def showImage(image):
	cv2.imshow('image',image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def hughTransform(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	lines = cv2.HoughLines(edges,1,np.pi/180,200)
	for rho,theta in lines[0]:
	    a = np.cos(theta)
	    b = np.sin(theta)
	    x0 = a*rho
	    y0 = b*rho
	    x1 = int(x0 + 1000*(-b))
	    y1 = int(y0 + 1000*(a))
	    x2 = int(x0 - 1000*(-b))
	    y2 = int(y0 - 1000*(a))

	    cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
	return image

def hughTransformP(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	gray = gaussianBlur(gray,5)
	gray = adjustGamma(gray,0.7)
	#gray = globalThreshold(gray,127)
	
	edges = cv2.Canny(gray,30,100,apertureSize = 3)
	
	minLineLength = 10
	maxLineGap = 20
	lines = cv2.HoughLinesP(edges,1,np.pi/180,90,minLineLength,maxLineGap)
	for x1,y1,x2,y2 in lines[0]:
	    cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
	#showImage(image)
	return image

def canny(image,minLen,maxLen):
	return cv2.Canny(image,minLen,maxLen)

def smoothenImage(img,kernel):
	img = gaussianBlur(img,kernel)
	return img

def flipHorizontal(img):
	return cv2.flip(img,1)

def flipVertical(img):
	return cv2.flip(img,0)

def findContours(img):
	#img = convertToGray(img)
	edges = canny(img,10,100)
	contours, hierarchy = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return contours

def drawAllContours(image,contours):
	cv2.drawContours(image, contours, -1, (0,255,0), 1)

def drawContour(image,contour):
	return cv2.drawContours(image, [contour], 0, (0,255,0), 1)

def getImage(inputDir):
	filelist= [file for file in os.listdir(inputDir) if file.endswith('.png')]
	return filelist

def adaptiveThreshold(img):
	return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)

def adaptiveThresholdGuassian(img):
	return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

# file IO
def saveImage(outputDir,filename,image):
	cv2.imwrite(outputDir+"/"+filename,image);

def createDir(outputDir):
	print "checking dir"
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)
		print "dir created"

def removeFiles(dir):
	files = os.listdir(dir)
	for file in files:
		os.remove(dir+"/"+file)


def adjustGamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")

	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)


def perspectiveTransformation(image):
	rows,cols,ch = image.shape

	pts1 = np.float32([[156,65],[368,52],[128,387],[389,390]])
	pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(image,M,(500,268))
	return dst




if __name__ == "__main__":

	if(len(sys.argv) > 2):
		inputDir = sys.argv[1]
		outputDir = sys.argv[2]

		createDir(outputDir)
		# call road detection method
		#removeFiles(outputDir)
		roadMarkDetect(inputDir,outputDir)
	else:
		print "[INFO] : params required : contour_road.py <inputDir> <outputDir>"


