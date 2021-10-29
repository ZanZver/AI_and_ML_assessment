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
        #startup.DV.createMap
        try:
            print("Creating a map")
            errorCreation, mapCreation = globalVar.createMap()
            if(errorCreation == 0):
                pass
            elif(errorCreation == 1):
                print("Error 1 caught on map creation")
                
        except Exception as e:
            print("Error creating map")
            print("Error code: " + str(e))

        fileLocation = ""
        try:
            fileLocation = startup.os.path.realpath("map.html")
        except FileNotFoundError:
            print("File not found! Please check if map.html has been created")
        except Exception as e:
            print("Error has occurred on getting file path.")
            print("Error message: " + str(e))
        self.browser.setUrl(QUrl(str("file://") + str(fileLocation)))

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
        originStr = str(self.originSrc.text()).strip()
        if not originStr:
            return(int(1), str(""))
        else:
            return[int(0), str(originStr)]

    def getDestination(self):
        destinationStr = str(self.destinationSrc.text()).strip()
        if not destinationStr:
            return(int(1), str(""))
        else:
            return[int(0), str(destinationStr)]

    def findAll(self):
        originError, originStr = self.getOrigin()
        destinationError, destinationStr = self.getDestination()
        if(((int(originError)) == 0) and ((int(destinationError)) == 0)):
            if(str(originStr) == str(destinationStr)):
                print("Please select two different locations for program to work")
            else:
                answer = (globalVar.getPath(str(originStr), str(destinationStr)))
                if answer == 0:
                    self.browser.reload()
                else:
                    print("Error getting path")
        elif((int(originError) == 1) and (int(destinationError) == 1)):
            print("Origin and destination are empty, please fill it in")
        elif(int(originError) == 1):
            print("Origin is empty, please fill it in")
        elif(int(destinationError) == 1):
            print("Destination is empty, please fill it in")
        else:
            print("Error with origin and destination, check it again please")

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