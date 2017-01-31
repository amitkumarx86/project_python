import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import cv2
import copy
import os

class ImageProcessor(QMainWindow):
    
    global image, l1, grayScaleBtn, gaussianBlurBtn, cannyBtn, houghPBtn, houghBtn, sobelXBtn, sobelYBtn, laplacianBtn,\
    simpleThresBtn, adaptiveThresGaussianBtn, otsuThresBtn, adaptiveMeanThresBtn, undoBtn, saveBtn

    # stack for undo
    global imageStack, buttonStack
    global filelist

    ########################################################################
    #                   UI functions
    ########################################################################
    def __init__(self, parent = None):
        super(ImageProcessor, self).__init__(parent)

        layout = QHBoxLayout()
        
        self.filelist= [file for file in os.listdir('./') if file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.jpg')]
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
        self.l1.resize(1000, 1000)
    	
        # pallet for save button
        self.savePallet = QDockWidget("Image",self)
        self.savePallet.setFloating(False)
        self.savePallet.setFeatures(QDockWidget.DockWidgetMovable)
        self.savePallet.resize(QSize(100, 100))

        self.saveBtn = QPushButton("Save")
        self.saveBtn.setMaximumWidth(100)
        
        
        saveIcon = QIcon()
        saveIcon.addPixmap(QPixmap("./icons/save.png"))
        
        self.saveBtn.setIcon(saveIcon)
        self.saveBtn.setStyleSheet('QPushButton { background-color: #04942a; border-color: #0b6d13;}')
        self.saveBtn.clicked.connect(self.saveFun)
        self.multiWidget = QWidget()
        self.vbox = QVBoxLayout()
        
        self.vbox.addWidget(self.l1)
        self.vbox.addWidget(self.saveBtn)
        
        #self.hbox.addStretch()
        #self.hbox.addWidget(self.saveBtn)
        
        #self.multiWidgetBottom.setLayout(self.hbox)


        #self.vbox.addWidget(self.multiWidgetBottom)
        self.multiWidget.setLayout(self.vbox)

        #self.savePallet.setWidget(self.multiWidget)
        # adding pallet and QLabel to main window
        
        self.setCentralWidget(self.multiWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.pallet)
        self.setGeometry(0,0,2000,2000)
        self.setWindowTitle("Image Processor")
        self.imageStack=list()
        self.buttonStack=list()

    def addMenuInWindow(self):
        bar = self.menuBar()
        file = bar.addMenu("File")

        openFile = QAction("Open",self)
        openFile.setShortcut("Ctrl+O")
        openFile.triggered.connect(self.getImage)
        file.addAction(openFile)
        
        quit = QAction("Quit",self)
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

        
        self.gaussianBlurBtn = QPushButton("Gaussian Blur")
        self.gaussianBlurBtn.clicked.connect(self.gaussianBlurFun)

        
        self.cannyBtn = QPushButton("Canny Edge Detection")
        self.cannyBtn.clicked.connect(self.cannyFun)

        self.houghPBtn = QPushButton("Hough P Line Detection")
        self.houghPBtn.clicked.connect(self.houghPFun)

        self.houghBtn = QPushButton("Hough Line Detection")
        self.houghBtn.clicked.connect(self.houghFun)


        self.sobelXBtn = QPushButton("SobelX Edge Detection")
        self.sobelXBtn.clicked.connect(self.sobelXFun)

        self.sobelYBtn = QPushButton("SobelY Edge Detection")
        self.sobelYBtn.clicked.connect(self.sobelYFun)

        self.laplacianBtn = QPushButton("Laplacian Edge Detection")
        self.laplacianBtn.clicked.connect(self.laplacianFun)
        

        # undo and save buttons
        undoAndSaveParent = QWidget()
        self.undoBtn = QPushButton("Undo")
        icon = QIcon()
        icon.addPixmap(QPixmap("./icons/undo.png"))
        self.undoBtn.setIcon(icon)
        self.undoBtn.clicked.connect(self.undoFun)

        
        
        self.nextBtn = QPushButton("Next")
        nextIcon = QIcon()
        nextIcon.addPixmap(QPixmap("./icons/next.png"))
        self.nextBtn.setIcon(nextIcon)
        self.nextBtn.setStyleSheet('QPushButton { background-color: #5033c5; border-color: #0b6d13;}')
        self.nextBtn.clicked.connect(self.nextPic)
        

        hbox = QHBoxLayout()
        hbox.addWidget(self.undoBtn)
        hbox.addWidget(self.nextBtn)
        #hbox.addWidget(self.saveBtn)
        undoAndSaveParent.setLayout(hbox)

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
        
        vbox.addWidget(self.gaussianBlurBtn)
        vbox.addStretch()
        vbox.addWidget(self.cannyBtn)
        vbox.addStretch()
        vbox.addWidget(self.sobelXBtn)
        vbox.addStretch()
        vbox.addWidget(self.sobelYBtn)
        vbox.addStretch()
        vbox.addWidget(self.laplacianBtn)
        vbox.addStretch()
        vbox.addWidget(self.houghPBtn)
        vbox.addStretch()
        vbox.addWidget(self.houghBtn)
        vbox.addStretch()
        vbox.addStretch()
        vbox.addStretch()
        vbox.addStretch()
        vbox.addStretch()
        vbox.addWidget(undoAndSaveParent)
        


        multiWidget.setLayout(vbox)
        pallet.setWidget(multiWidget)
        # disable all button before use
        self.toggleOperatorButtons(False)

	
    ########################################################################
    #                   image processing functions
    ########################################################################
    def nextPic(self):
    	if(len(self.filelist) > 0):
			fname=self.filelist.pop()
			self.l1.setPixmap(QPixmap(fname).scaled(self.l1.size(), Qt.KeepAspectRatio)) # this command works like a charm
			self.l1.adjustSize()     
			self.image=cv2.imread(str(fname))
			self.toggleOperatorButtons(True)

    def saveFun(self):
		if not os.path.exists("output"):
			os.makedirs("output")
		cv2.imwrite('./output/output.jpg',self.image)
		self.showdialog("image is saved successfully.","Information")

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','./',"Image files (*.jpg *.gif *.jpeg *.png)")
        self.l1.setPixmap(QPixmap(fname).scaled(self.l1.size(), Qt.KeepAspectRatio)) # this command works like a charm
        self.l1.adjustSize()     
        self.image=cv2.imread(str(fname))
        self.toggleOperatorButtons(True)
    
    def toggleOperatorButtons(self,boolean):
        for button in [self.grayScaleBtn, self.gaussianBlurBtn, self.cannyBtn, self.houghPBtn, self.houghBtn, self.sobelXBtn, \
        self.sobelYBtn, self.laplacianBtn, self.adaptiveThresGaussianBtn, self.adaptiveMeanThresBtn,self.simpleThresBtn, self.otsuThresBtn\
        , self.undoBtn]:
            button.setEnabled(boolean)
            if(boolean):
              #  if(button == self.saveBtn):
             #       button.setStyleSheet('QPushButton { background-color: #04942a; border-color: #0b6d13;}')
                #else:    
                button.setStyleSheet('QPushButton { background-color: #0077dd; border-color: #07c;}')
            else:
                button.setStyleSheet('QPushButton { background-color: #5a778c; border-color: #07c; color : #fff}')
    
    def showImage(self,buttonName,image,toggle=False):
        
        if(not toggle):
            fname='temp.jpg'
            cv2.imwrite(fname,image)    
            self.l1.setPixmap(QPixmap(fname).scaled(self.l1.size(), Qt.KeepAspectRatio))
            buttonName.setStyleSheet('QPushButton {background-color: #34b31d; color : #fff}')
            buttonName.setEnabled(False)
        else:
            fname='temp.jpg'
            cv2.imwrite(fname,image)
            self.l1.setPixmap(QPixmap(fname).scaled(self.l1.size(), Qt.KeepAspectRatio))
            buttonName.setStyleSheet('QPushButton {background-color: #0077dd; border-color: #07c;}')
            buttonName.setEnabled(True)

    def undoFun(self):
        if(len(self.imageStack) > 0 ):
            self.image = self.imageStack.pop()
            button = self.buttonStack.pop()
            self.showImage(button,self.image,True)
        

    def grayFunc(self):
            if (len(self.image.shape) > 2):                
                # log for undo
                temp_image=copy.copy(self.image)
                self.imageStack.append(temp_image)
                self.buttonStack.append(self.grayScaleBtn)

                self.image=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) 
                self.showImage(self.grayScaleBtn,self.image)
                #self.showdialog("done :)","Information")
            else: 
                self.showdialog("image is already converted to gray.","Critical")

    def simpleThresFun(self):
        if(len(self.image.shape) > 2):
            minThresVal = self.getNumberFromUser("Threshold","Enter val (eg. 127)",127)
            if(minThresVal > 0 and minThresVal < 255):
                # log for undo
                temp_image=copy.copy(self.image)
                self.imageStack.append(temp_image)
                self.buttonStack.append(self.simpleThresBtn)

                gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
                ret, self.image = cv2.threshold(gray,minThresVal,255,cv2.THRESH_BINARY)
                self.showImage(self.simpleThresBtn,self.image)
                #self.showdialog("done :)","Information")
            else:
                self.showdialog("Threshold not correct, try again.","Warning")        
        else:
            self.showdialog("image is already converted to gray, undo.","Warning") 

    def adaptiveMeanThresFun(self):
        if(len(self.image.shape) > 2):
            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.adaptiveMeanThresBtn)

            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
            self.showImage(self.adaptiveMeanThresBtn,self.image)
            #self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, undo.","Warning") 

    def adaptiveThresGaussianFun(self):
        if(len(self.image.shape) > 2):
            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.adaptiveThresGaussianBtn)
            
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
            self.showImage(self.adaptiveThresGaussianBtn,self.image)
            #self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning") 

    def otsuThresFun(self):
        if(len(self.image.shape) > 2):
            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.otsuThresBtn)
            
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            ret3, self.image  = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            self.showImage(self.otsuThresBtn,self.image)
            #self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, undo.","Warning") 

    def laplacianFun(self):
        if(len(self.image.shape) > 2):
            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.laplacianBtn)

            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.Laplacian(gray,cv2.CV_64F)
            self.showImage(self.laplacianBtn,self.image)
            #self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, undo.","Warning") 

    def sobelXFun(self):
        if(len(self.image.shape) > 2):
            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.sobelXBtn)

            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
            self.showImage(self.sobelXBtn,self.image)
            #self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, undo.","Warning")
    
    def sobelYFun(self):
        if(len(self.image.shape) > 2):
            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.sobelYBtn)

            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.image = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5)
            self.showImage(self.sobelYBtn,self.image)
            #self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, undo.","Warning")

    def cannyFun(self):
        if(len(self.image.shape) > 2):
            minVal = self.getNumberFromUser("Kernel Size","Enter minVal (eg. 10)",10)
            maxVal = self.getNumberFromUser("Kernel Size","Enter maxVal (eg. 100)",100)
            if(minVal > 0 and maxVal > 80):

                # log for undo
                temp_image=copy.copy(self.image)
                self.imageStack.append(temp_image)
                self.buttonStack.append(self.cannyBtn)

                self.image=cv2.Canny(self.image,minVal,maxVal)
                self.showImage(self.cannyBtn,self.image)
                #self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, cannot perform canny.","Warning")

    def houghFun(self):
        if(len(self.image.shape) > 2):

            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.houghBtn)
            
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

            self.showImage(self.houghBtn,self.image)
            self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, cannot perform hough line detection.","Warning")

    def houghPFun(self):   
        if(len(self.image.shape) > 2):

            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.houghPBtn)

            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray,50,150,apertureSize = 3)
            minLineLength = 100
            maxLineGap = 10
            lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
            for x1,y1,x2,y2 in lines[0]:
                cv2.line(self.image,(x1,y1),(x2,y2),(0,255,0),2)

            self.showImage(self.houghPBtn,self.image)
            self.showdialog("done :)","Information")
        else:
            self.showdialog("image is already converted to gray, cannot perform hough P line detection.","Warning")

    

    def gaussianBlurFun(self):
        kernel = self.getNumberFromUser("Kernel Size","Enter an Odd Number",3)
        if kernel % 2 != 0 and kernel < 20:

            # log for undo
            temp_image=copy.copy(self.image)
            self.imageStack.append(temp_image)
            self.buttonStack.append(self.gaussianBlurBtn)

            self.image=cv2.GaussianBlur(self.image,(kernel,kernel),0)
            self.showImage(self.gaussianBlurBtn,self.image)            
            #self.showdialog("done :)","Information")
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
        
        msg.setText(input)
        msg.setInformativeText("            ")
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