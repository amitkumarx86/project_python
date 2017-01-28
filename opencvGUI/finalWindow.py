import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import cv2
  

class ImageProcessor(QMainWindow):
    
    global image, l1, grayScaleBtn, guassianBlurBtn, cannyBtn, hughPBtn, hughBtn, sobelXBtn, sobelYBtn, laplacianBtn,\
    simpleThresBtn, adaptiveThresGaussianBtn, otsuThresBtn, adaptiveMeanThresBtn


    ########################################################################
    #                   UI functions
    ########################################################################
    def __init__(self, parent = None):
        super(ImageProcessor, self).__init__(parent)

        layout = QHBoxLayout()
        
        self.graycount=0
        #cv2.imshow('asdf',image)

        # add menu 
        self.addMenuInWindow()
        #function pallet
        self.pallet = QDockWidget("OpenCV Functions", self)
        self.pallet.setFloating(False)
        self.pallet.setFeatures(QDockWidget.DockWidgetMovable) # this makes pallet not rigid
        # adding buttons to pallet
        self.designPallet(self.pallet)


        
        # PixMap image label
        self.l1 = QLabel()

        # adding pallet and QLabel
        self.setCentralWidget(self.l1)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.pallet)
        self.setGeometry(0,0,2000,2000)
        self.setWindowTitle("Image Processor")
    
    def addMenuInWindow(self):
        bar = self.menuBar()
        file = bar.addMenu("File")

        openFile = QAction("Open",self)
        openFile.setShortcut("Ctrl+O")
        openFile.triggered.connect(self.getImage)
        file.addAction(openFile)
        
        quit = QAction("quit",self)
        quit.setShortcut("Ctrl+Q")
        quit.triggered.connect(self.closingFun)
        file.addAction(quit)         

    def closingFun(self):
        retval = self.showdialog("Are you sure to exit","Question")
        if (retval == 1024):
            self.close()

    def designPallet(self,pallet):
        multiWidget = QWidget()
        self.grayScaleBtn = QPushButton("Gray")
        self.grayScaleBtn.clicked.connect(self.grayFunc)

        self.simpleThresBtn = QPushButton("SimpleThresholding")
        self.simpleThresBtn.clicked.connect(self.simpleThresFun)

        self.adaptiveMeanThresBtn = QPushButton("Adaptive Thresholding")
        self.adaptiveMeanThresBtn.clicked.connect(self.adaptiveMeanThresFun)

        self.adaptiveThresGaussianBtn = QPushButton("Adaptive Gaussian Thresholding")
        self.adaptiveThresGaussianBtn.clicked.connect(self.adaptiveThresGaussianFun)

        self.otsuThresBtn = QPushButton("Otsu's Binarization")
        self.otsuThresBtn.clicked.connect(self.otsuThresFun)

        
        self.guassianBlurBtn = QPushButton("Guassian Blur")
        self.guassianBlurBtn.clicked.connect(self.guassianBlurFun)


        
        self.cannyBtn = QPushButton("Canny Edge Detection")
        self.cannyBtn.clicked.connect(self.cannyFun)

        self.hughPBtn = QPushButton("Hugh P Line Detection")
        self.hughPBtn.clicked.connect(self.hughPFun)
        self.hughBtn = QPushButton("Hugh Line Detection")
        self.hughBtn.clicked.connect(self.hughFun)


        self.sobelXBtn = QPushButton("SobelX Edge Detection")
        self.sobelXBtn.clicked.connect(self.sobelXFun)

        self.sobelYBtn = QPushButton("SobelY Edge Detection")
        self.sobelYBtn.clicked.connect(self.sobelYFun)

        self.laplacianBtn = QPushButton("Laplacian Edge Detection")
        self.laplacianBtn.clicked.connect(self.laplacianFun)


        vbox = QVBoxLayout()
        vbox.addWidget(self.grayScaleBtn)
        vbox.addStretch()
        vbox.addWidget(self.simpleThresBtn)
        vbox.addStretch()
        vbox.addWidget(self.adaptiveMeanThresBtn)
        vbox.addStretch()
        vbox.addWidget(self.adaptiveThresGaussianBtn)
        vbox.addStretch()
        vbox.addWidget(self.otsuThresBtn)
        vbox.addStretch()
        
        vbox.addWidget(self.guassianBlurBtn)
        vbox.addStretch()
        vbox.addWidget(self.cannyBtn)
        vbox.addStretch()
        vbox.addWidget(self.sobelXBtn)
        vbox.addStretch()
        vbox.addWidget(self.sobelYBtn)
        vbox.addStretch()
        vbox.addWidget(self.laplacianBtn)
        vbox.addStretch()
        vbox.addWidget(self.hughPBtn)
        vbox.addStretch()
        vbox.addWidget(self.hughBtn)

        multiWidget.setLayout(vbox)
        pallet.setWidget(multiWidget)
        # disable all button before use
        self.toggleOperatorButtons(False)

    ########################################################################
    #                   image processing functions
    ########################################################################
    
    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','./',"Image files (*.jpg *.gif *.jpeg *.png)")
        self.l1.setPixmap(QPixmap(fname).scaled(self.l1.size(), Qt.KeepAspectRatio)) # this command works like a charm
        self.l1.adjustSize()     
        self.image=cv2.imread(str(fname))
        self.toggleOperatorButtons(True)
    
    def toggleOperatorButtons(self,boolean):
        for button in [self.grayScaleBtn, self.guassianBlurBtn, self.cannyBtn, self.hughPBtn, self.hughBtn, self.sobelXBtn, \
        self.sobelYBtn, self.laplacianBtn, self.adaptiveThresGaussianBtn, self.adaptiveMeanThresBtn,self.simpleThresBtn, self.otsuThresBtn]:
            button.setEnabled(boolean)
            if(boolean):
                button.setStyleSheet('QPushButton { background-color: #0077dd; border-color: #07c;}')
            else:
                button.setStyleSheet('QPushButton { background-color: #5a778c; border-color: #07c; color : #fff}')
    
    def showImage(self,buttonName,image):
        fname='temp.jpg'
        cv2.imwrite(fname,image)
        self.l1.setPixmap(QPixmap(fname).scaled(self.l1.size(), Qt.KeepAspectRatio))
        buttonName.setStyleSheet('QPushButton {background-color: #34b31d; color : #fff}')
        buttonName.setEnabled(False)
    
    def simpleThresFun(self):
        if(len(self.image.shape) > 2):
            minThresVal = self.getNumberFromUser("Threshold","Enter val (eg. 127)",127)
            if(minThresVal > 50):
                gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
                ret, self.image = cv2.threshold(gray,minThresVal,255,cv2.THRESH_BINARY)
                self.showImage(self.simpleThresBtn,self.image)
            else:
                self.showdialog("Threshold not correct, try again.","Warning")        
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning") 

    def adaptiveMeanThresFun(self):
        if(len(self.image.shape) > 2):
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
            self.showImage(self.adaptiveMeanThresBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning") 

    def adaptiveThresGaussianFun(self):
        if(len(self.image.shape) > 2):
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
            self.showImage(self.adaptiveThresGaussianBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning") 

    def otsuThresFun(self):
        if(len(self.image.shape) > 2):
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            ret3, self.image  = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.showImage(self.otsuThresBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning") 

    def laplacianFun(self):
        if(len(self.image.shape) > 2):
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.Laplacian(gray,cv2.CV_64F)
            self.showImage(self.laplacianBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning") 

    def sobelXFun(self):
        if(len(self.image.shape) > 2):
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
            self.showImage(self.sobelXBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning")
    
    def sobelYFun(self):
        if(len(self.image.shape) > 2):
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5)
            self.showImage(self.sobelYBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning")

    def cannyFun(self):
        if(len(self.image.shape) > 2):
            minVal = self.getNumberFromUser("Kernel Size","Enter minVal (eg. 10)",10)
            maxVal = self.getNumberFromUser("Kernel Size","Enter maxVal (eg. 100)",100)
            if(minVal > 0 and maxVal > 80):
                self.image=cv2.Canny(self.image,minVal,maxVal)
                self.showImage(self.cannyBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning")

    def hughFun(self):
        if(len(self.image.shape) > 2):
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
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

                cv2.line(self.image,(x1,y1),(x2,y2),(0,0,255),2)

            self.showImage(self.hughBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform hugh line detection.","Warning")

    def hughPFun(self):   
        if(len(self.image.shape) > 2):
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray,50,150,apertureSize = 3)
            minLineLength = 100
            maxLineGap = 10
            lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
            for x1,y1,x2,y2 in lines[0]:
                cv2.line(self.image,(x1,y1),(x2,y2),(0,255,0),2)

            self.showImage(self.hughPBtn,self.image)
        else:
            self.showdialog("image is already converted to gray, cannot perform hugh P line detection.","Warning")

    

    def guassianBlurFun(self):
        kernel = self.getNumberFromUser("Kernel Size","Enter an Odd Number",3)
        if kernel % 2 != 0 and kernel < 20:
            self.image=cv2.GaussianBlur(self.image,(kernel,kernel),0)
            self.showImage(self.guassianBlurBtn,self.image)            
        else:
            self.showdialog("Kernel Size should be odd or less than 23","Warning")
    
    # show warning if kernel size is not odd
    def showdialog(self,input,type):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        if(type=="Warning"):
            msg.setIcon(QMessageBox.Warning)
        elif (type=="Critical"):
            msg.setIcon(QMessageBox.Critical)
        elif (type=="Information"):
            msg.setIcon(QMessageBox.Information)
        else:
            msg.setIcon(QMessageBox.Question)
        #msg.setText(type)
        msg.setInformativeText(input)
        msg.setStandardButtons(QMessageBox.Ok) 
        
        if(type=="Question"):
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        
        msg.setWindowTitle(type)   
        retval = msg.exec_()
        return retval

    def getNumberFromUser(self,Type,Entry,defaultVal):
        num,ok = QInputDialog.getInt(self,Type,Entry,defaultVal)
        if ok:
            return num

    def grayFunc(self):
        if (len(self.image.shape) > 2):
            self.image=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) 
            self.showImage(self.grayScaleBtn,self.image)
        else: 
            self.showdialog("image is already converted to gray.","Critical")
        
    
# class ImageProcessor Ends here

########################################################################
#                   Driver Function
########################################################################
def main():
   app = QApplication(sys.argv)
   ex = ImageProcessor()
   ex.show()
   sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()