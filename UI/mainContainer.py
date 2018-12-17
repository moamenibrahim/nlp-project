from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import UI.iconsLauncher
import UI.mainWindow
import sys
import os

class mainContainer(QMainWindow):
    """This class acts as the main container of any subwindow,
    that can be implemented inside of it.
    
    Arguments:
        QMainWindow {class} -- inheriting from QMainWindow class.
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
        return

    def initUI(self):
        self.setWindowIcon(QIcon(UI.iconsLauncher.getIcon('mainIcon', OS = sys.platform)))
        self.setWindowTitle("Natural Language Processing")

        # self.FMainMenu_init()
        self.showNormal()
        # self.width = 640
        # self.height = 600
        # self.left = 100
        # self.top = 100
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.stat)
        self.mainWindow = UI.mainWindow.mainWindow(self)
        self.setCentralWidget(self.mainWindow)


