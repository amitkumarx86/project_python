import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import cv2
  

class ImageProcessor(QMainWindow):
    
    global image, l1, graycount, grayScaleBtn, guassianBlurBtn, cannyBtn, hughPBtn, hughBtn

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
        quit.triggered.connect(self.close)
        file.addAction(quit)         

    def designPallet(self,pallet):
        multiWidget = QWidget()
        self.grayScaleBtn = QPushButton("Gray")
        self.grayScaleBtn.clicked.connect(self.grayFunc)

        self.guassianBlurBtn = QPushButton("Guassian Blur")
        self.guassianBlurBtn.clicked.connect(self.guassianBlurFun)

        
        self.cannyBtn = QPushButton("Canny Edge Detection")
        self.cannyBtn.clicked.connect(self.cannyFun)

        self.hughPBtn = QPushButton("Hugh P Line Detection")
        self.hughPBtn.clicked.connect(self.hughPFun)
        self.hughBtn = QPushButton("Hugh Line Detection")
        self.hughBtn.clicked.connect(self.hughFun)


        self.SobelOperatorBtn = QPushButton("Sobel Edge Detection")
        self.SobelOperatorBtn.clicked.connect(self.SobelOperatorFun)


        vbox = QVBoxLayout()
        vbox.addWidget(self.grayScaleBtn)
        vbox.addStretch()
        vbox.addWidget(self.guassianBlurBtn)
        vbox.addStretch()
        vbox.addWidget(self.cannyBtn)
        vbox.addStretch()
        vbox.addWidget(self.SobelOperatorBtn)
        vbox.addStretch()
        vbox.addWidget(self.hughPBtn)
        vbox.addStretch()
        vbox.addWidget(self.hughBtn)

        multiWidget.setLayout(vbox)
        pallet.setWidget(multiWidget)


    ########################################################################
    #                   image processing functions
    ########################################################################
    
    def showImage(self,buttonName,image):
        fname='temp.jpg'
        cv2.imwrite(fname,image)
        self.l1.setPixmap(QPixmap(fname).scaled(self.l1.size(), Qt.KeepAspectRatio))
        buttonName.setStyleSheet('QPushButton {background-color: green;}')
        buttonName.setEnabled(False)
    
    def cannyFun(self):
        self.image=cv2.Canny(self.image,10,100)
        self.showImage(self.cannyBtn,self.image)
        
    def hughFun(self):
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

    def hughPFun(self):   
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        minLineLength = 100
        maxLineGap = 10
        lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(self.image,(x1,y1),(x2,y2),(0,255,0),2)

        self.showImage(self.hughPBtn,self.image)
        
    def SobelOperatorFun():
        print "SobelOperatorFun"


    def guassianBlurFun(self):
        kernel = self.getKernelSize()
        if kernel % 2 != 0 :
            self.image=cv2.GaussianBlur(self.image,(kernel,kernel),0)
            self.showImage(self.guassianBlurBtn,self.image)            
        else:
            self.showdialog()
    
    # show warning if kernel size is not odd
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Warning")
        msg.setInformativeText("Kernel Size should be odd")
        msg.setStandardButtons(QMessageBox.Ok)    
        retval = msg.exec_()

    def getKernelSize(self):
        num,ok = QInputDialog.getInt(self,"Kernel Size","enter an odd number")
        if ok:
            return num

    def grayFunc(self):
        if (self.graycount==0):
            self.graycount=1
            self.image=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) 
            self.showImage(self.grayScaleBtn,self.image)
        
    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','./',"Image files (*.jpg *.gif *.jpeg *.png)")
        self.l1.setPixmap(QPixmap(fname).scaled(self.l1.size(), Qt.KeepAspectRatio))
        self.l1.adjustSize()     
        self.image=cv2.imread(str(fname))
    
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