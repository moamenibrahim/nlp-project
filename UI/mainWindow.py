from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.qrangeslider import QRangeSlider
import main
import viewer


class mainWindow(QDialog):
    """This class will hold buttons and checkboxes
    to specify parameters as inputs to the program
    
    Arguments:
        QDialog {[Class]} -- PyQt parent class
    """
    
    def __init__(self, parent):
        QDialog.__init__(self)
        self.parent = parent
        self.layout = QGridLayout()

        self.rangeSlider = QRangeSlider()
        self.rangeSlider.setRange(2001,2015)
        self.rangeSlider.setMin(2001)
        self.rangeSlider.setMax(2015)

        self.TNE = QPushButton("Top Named Entities", self)
        self.TNE.setCheckable(True)
        self.TNE.setChecked(False)
        self.TNE.setStatusTip("Runs Top Named entities algorithm")
        
        self.SA = QPushButton("Sentiment Analysis", self)
        self.SA.setCheckable(True)
        self.SA.setChecked(False)
        self.SA.setStatusTip("Runs Sentiment Analysis algorithm")


        self.LDA = QPushButton("LDA", self)
        self.LDA.setCheckable(True)
        self.LDA.setChecked(False)
        self.LDA.setStatusTip("Runs LDA algorithm")

        self.TC = QPushButton("Top Co-occurences", self)
        self.TC.setCheckable(True)
        self.TC.setChecked(False)
        self.TC.setStatusTip("Runs Top Co-occurences algorithm")

        self.TD = QPushButton("Top Diseases", self)
        self.TD.setCheckable(True)
        self.TD.setChecked(False)
        self.TD.setStatusTip("Runs Top Diseases algorithm")

        self.executeBTN = QPushButton("Execute Selected")
        self.executeBTN.clicked.connect(self.executeSelected)
        self.executeBTN.setStatusTip("Executes Selected algorithms")

        self.layout.addWidget(self.rangeSlider, 0, 0, Qt.AlignTop)
        self.layout.addWidget(self.TNE, 1,0)
        self.layout.addWidget(self.SA , 2, 0)
        self.layout.addWidget(self.LDA , 3, 0)
        self.layout.addWidget(self.TC , 4, 0)
        self.layout.addWidget(self.TD , 5, 0)
        self.layout.addWidget(self.executeBTN, 6, 0)

        self.setLayout(self.layout)
        

    def executeSelected(self):
        rangeMin, rangeMax = self.rangeSlider.getRange()
        print(rangeMin, " ", rangeMax)
        self.dataAll = dict()
        if(self.TNE.isChecked()):
            self.executeTNE(rangeMin, rangeMax, self.dataAll)
        
        if(self.SA.isChecked()):
            self.executeSA(rangeMin, rangeMax, self.dataAll)

        if(self.LDA.isChecked()):
            self.executeLDA(rangeMin, rangeMax, self.dataAll)

        if(self.TC.isChecked()):
            self.executeTC(rangeMin, rangeMax, self.dataAll)

        if(self.TD.isChecked()):
            self.executeTD(rangeMin, rangeMax, self.dataAll)

        # if (not len(self.dataAll)):
        #     return
        # else:
        #     self.dataViewer = viewer.viewer(self)
        #     self.setCentralWidget(self.dataViewer)
        #     self.setWindowTitle("Results Viewer")
        return
###########################################################################
    def executeTNE(self, rangeMin, rangeMax, dataOutDict):
        print("TNE activated")
        ## data should be a list of tuples, where each tuple is (string, int)
        # data = main.histogramNER()
        # dataOutDict['TNE'] = data
        return


    def executeSA(self, rangeMin, rangeMax, dataOutDict):
        print("SA activated")
        ## data should be a list of tuples, where each tuple is (int, int)
        # data = main.getSent()
        # dataOutDict['SA'] = data
        return

    def executeLDA(self, rangeMin, rangeMax, dataOutDict):
        print("LDA activated")
        ## data should be a string
        # data = main.getTopic()
        # dataOutDict['LDA'] = data
        return

    def executeTC(self, rangeMin, rangeMax, dataOutDict):
        print("TC activated")
        ## data is a list of tuples, where each tuple is (string, int)
        # data = main.mostCooccuring()
        # dataOutDict['TC'] = data
        return

    def executeTD(self, rangeMin, rangeMax, dataOutDict):
        ## TODO
        print("TD activated")
        print("Future work: not yet designed.")
        return