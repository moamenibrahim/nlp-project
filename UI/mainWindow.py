from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.qrangeslider import QRangeSlider

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
        
        self.SA = QPushButton("Sentiment Analysis", self)
        self.SA.setCheckable(True)
        self.SA.setChecked(False)

        self.LDA = QPushButton("LDA", self)
        self.LDA.setCheckable(True)
        self.LDA.setChecked(False)

        self.TC = QPushButton("Top Co-occurences", self)
        self.TC.setCheckable(True)
        self.TC.setChecked(False)

        self.TD = QPushButton("Top Diseases", self)
        self.TD.setCheckable(True)
        self.TD.setChecked(False)

        self.executeBTN = QPushButton("Execute Selected")
        self.executeBTN.clicked.connect(self.executeSelected)

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
        if(self.TNE.isChecked()):
            self.executeTNE(rangeMin, rangeMax)
        
        if(self.SA.isChecked()):
            self.executeSA(rangeMin, rangeMax)

        if(self.LDA.isChecked()):
            self.executeLDA(rangeMin, rangeMax)

        if(self.TC.isChecked()):
            self.executeTC(rangeMin, rangeMax)

        if(self.TD.isChecked()):
            self.executeTD(rangeMin, rangeMax)

        return
###########################################################################
    def executeTNE(self, rangeMin, rangeMax):
        ## TODO
        print("TNE activated")
        return


    def executeSA(self, rangeMin, rangeMax):
        ## TODO
        print("SA activated")
        return

    def executeLDA(self, rangeMin, rangeMax):
        ## TODO
        print("LDA activated")
        return

    def executeTC(self, rangeMin, rangeMax):
        ## TODO
        print("TC activated")
        return

    def executeTD(self, rangeMin, rangeMax):
        ## TODO
        print("TD activated")
        return