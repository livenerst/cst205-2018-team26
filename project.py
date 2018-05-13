
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QTextBrowser, QGroupBox, QScrollArea, QComboBox
from urllib.request import Request,urlopen
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QColor
from functools import partial
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import requests
import sys
import ssl
from joff_filter import *
import cv2
import numpy as np

global pic
global image
global buttons

class Window1(QWidget):
    def __init__(self):
        super().__init__()
        #backgroud
        # self.setAutoFillBackground(True)
        # p = self.palette()
        # p.setColor(self.backgroudRole(),QColor(227,66,52))
        # self.setPalette(p)
        #title of the Application
        self.setWindowTitle('Search Image Url')
        QWidget.setGeometry(self,45,45,400,300)

        self.pic = []
        self.image = []
        self.buttons = []

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        #search bar
        self.searchBar = QLabel('Search: ')
        self.mySearch = QLineEdit()

        # 'go button'
        self.searchButton = QPushButton('Go')
        self.searchButton.clicked.connect(self.goClicked)

        #'Search: ', Bar, Go Button
        hbox.addWidget(self.searchBar)
        hbox.addWidget(self.mySearch)
        hbox.addWidget(self.searchButton)
        vbox.addLayout(hbox)
        #self.setLayout(vbox)

        # scroll = QtGui.QScrollArea()
        # scroll.setWidget(QWidget)

        #Labels created
        for i in range(8):
            self.pic.append(QLabel())
            self.image.append(QPixmap())
            #setting the data on the pic list
            self.pic[i].setPixmap(self.image[i])
            self.button = QPushButton('Button',self)
            self.button.hide()
            vbox.addWidget(self.pic[i])
            vbox.addWidget(self.button)
            self.buttons.append(self.button)
         #Container Widget
        widget = QWidget()
        #Layout of Container Widget
        #layout = QVBoxLayout(self)
        widget.setLayout(vbox)

        #Scroll Area Properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        #Scroll Area Layer add
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)

        # vbox.addWidget(self.)

        #self.setLayout(vbox)

    @pyqtSlot()
    #when the 'go' button is clicked this function is called
    def goClicked(self):
        webLinks = []
        webSite = self.mySearch.text()
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        req = Request("https://" + webSite, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req,context=gcontext)
        bsObj = BeautifulSoup(html.read(),'lxml')
        #would the list slicing work for any website being scrapped
        for link in bsObj.findAll("img")[:8]:
                if 'src' in link.attrs:
                    webLinks.append(link.attrs['src'])
        #this for loop loop's through 3 lists: webLinks,image,pic at the same time
        for wl,image,pic,button in zip(webLinks,self.image, self.pic,self.buttons):
            #this grabs my links from my webLink
            response = requests.get(wl)
            #puts the data in the list in binary
            image.loadFromData(bytes(response.content))
            pic.setPixmap(image)
            opencv_image = np.asarray(bytearray(response.content), dtype="uint8")
            opencv_image = cv2.imdecode(opencv_image, cv2.IMREAD_COLOR)
            #takes in
            button.clicked.connect(partial(self.newWindow, img=image, img_cv=opencv_image))
            button.show()

    @pyqtSlot()
    def newWindow(self, **kwargs):
            self.goToWindow = filterImage(kwargs['img'],kwargs['img_cv'])
            self.goToWindow.show()

    # @pyqtSlot()
    # def pictureClicked:


#create a new window that displays the image that was clicked

filterList = ["Select", "red", "green", "blue", "grey filter progressive", "grey"]
filterFunctions = [redImage, greenImage, blueImage, grey_filter_progressive, grey_filter]
'''
filterImage made by Mason Emura
This class is the second window in our program
It displays the image that the user clicked
On this page the user can apply filters to that image
'''
class filterImage(QWidget):
    def __init__(self, img,img_cv):
        super().__init__()
        self.setWindowTitle('Filter Image')
        QWidget.setGeometry(self, 45, 45, 400, 300)
        hbox2 = QHBoxLayout()
        vbox2 = QVBoxLayout()
        self.button = QPushButton('Convert',self)
        self.filterDropdown = QComboBox()
        self.filterDropdown.addItems(filterList)
        self.filterDropdown.currentIndexChanged.connect(lambda : self.updateList(img_cv))
        self.dropdownLabel = QLabel("")
        self.image = QLabel()
        self.image.setPixmap(img)
        hbox2.addWidget(self.filterDropdown)
        hbox2.addWidget(self.dropdownLabel)
        vbox2.addWidget(self.image)
        vbox2.addLayout(hbox2)
        vbox2.addWidget(self.button)
        self.setLayout(vbox2)

    '''
    definition made by Mason Emura
    This grabs the image and index and depending on what filter the user choses
    it applies the filter to the image
    The filtered image is displayed in a new window
    '''
    @pyqtSlot()
    def updateList(self,image):
        chosenFilter = self.filterDropdown.currentText()
        chosenIndex = self.filterDropdown.currentIndex()
        temp = image.copy()
        if chosenIndex:
            cv2.imshow('image',filterFunctions[chosenIndex - 1](temp))


app = QApplication(sys.argv)
w = Window1()
w.show()
sys.exit(app.exec_())
