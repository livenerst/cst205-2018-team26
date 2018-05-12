from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QTextBrowser, QGroupBox
from urllib.request import Request,urlopen
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QColor
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import requests
import sys
import ssl

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

        # scroll = QtGui.QScrollArea()
        # scroll.setWidget(QWidget)

        #Labels created
        for i in range(8):
            self.pic.append(QLabel())
            self.image.append(QPixmap())
            #setting the data on the pic list
            self.pic[i].setPixmap(self.image[i])
            vbox.addWidget(self.pic[i])

        # vbox.addWidget(self.)

        self.setLayout(vbox)

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
                    print(webLinks)
        #this for loop loop's through 3 lists: webLinks,image,pic at the same time
        for wl,image,pic in zip(webLinks,self.image, self.pic):
            #this grabs my links from my webLink
            response = requests.get(wl)
            #puts the data in the list in binary
            image.loadFromData(bytes(response.content))
            pic.setPixmap(image)

    # @pyqtSlot()
    # def pictureClicked:


#create a new window that displays the image that was clicked
class filterImage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Filter Image')
        QWidget.setGeometry(self, 45, 45, 400, 300)





app = QApplication(sys.argv)
w = Window1()
w.show()
sys.exit(app.exec_())


# myUrl = input()

# im1 = Image.open("fruit1.jpg")
#
# def negRed(pixel):
#     return tuple(map(lambda a : 255 - a, pixel))
# negList = map(negRed, im1.getdata())
# im1.putdata(list(negList))
# im1.save("negativeRed.jpg")
