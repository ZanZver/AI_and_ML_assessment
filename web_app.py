#from startup import *
from PyQt5.QtWidgets import * 
from PyQt5.QtWebEngineWidgets import * 
from PyQt5.QtCore import *

try:
    import startup as startup
except Exception as e:
    print("startup.py not found. Stopping the code, please add it to the directory")
    print(e)
    sys.exit(1)

from startup import *
globalVar = ""

class Window(QMainWindow):

    #defining constructor function
    def __init__(self):
        #creating connnection with parent class constructor
        super(Window,self).__init__()

        #---------------------adding browser-------------------
        self.browser = QWebEngineView()
        
        #setting url for browser, you can use any other url also
        self.browser.setUrl(QUrl('file://' + startup.os.path.realpath("map.html")))

        #to display google search engine on our browser
        self.setCentralWidget(self.browser)

        #-------------------full screen mode------------------
        #to display browser in full screen mode, you may comment below line if you don't want to open your browser in full screen mode
        self.showMaximized()

        #----------------------navbar-------------------------
        #creating a navigation bar for the browser
        navbar = QToolBar()
        #adding created navbar
        self.addToolBar(navbar)

        #-----------refresh Button--------------------
        refreshBtn = QAction('Refresh',self)
        refreshBtn.triggered.connect(self.browser.reload)
        navbar.addAction(refreshBtn)

        #---------------------origin---------------------------------
        self.originLbl = QLabel(self)
        self.originLbl.setText("Origin")
        navbar.addWidget(self.originLbl)

        self.originSrc = QLineEdit()
        self.originSrc.setText("")
        
        #self.originSrc.returnPressed.connect(self.getOrigin)
        navbar.addWidget(self.originSrc)

        #---------------------destination---------------------------------
        self.destinationLbl = QLabel(self)
        self.destinationLbl.setText("Destination")
        navbar.addWidget(self.destinationLbl)

        self.destinationSrc = QLineEdit()
        self.destinationSrc.setText("")

        #self.destinationSrc.returnPressed.connect(self.getDestination)
        navbar.addWidget(self.destinationSrc)

        #-----------find Button--------------------
        findBtn = QAction('find',self)
        findBtn.triggered.connect(self.findAll)
        navbar.addAction(findBtn)

    def getOrigin(self):
        return(self.originSrc.text())

    def getDestination(self):
        return(self.destinationSrc.text())

    def findAll(self):
        #()
        answer = (globalVar.getPath(self.getOrigin(), self.getDestination()))
        if answer == 0:
            self.browser.reload()
        else:
            pass

def start(d1):
    global globalVar
    globalVar = d1

    MyApp = QApplication(startup.sys.argv)

    #setting application name
    QApplication.setApplicationName('Safe Walk')

    #creating window
    window = Window()

    #executing created app
    MyApp.exec_()