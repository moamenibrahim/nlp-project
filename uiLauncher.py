import sys
import os
import json
import numpy as np
# import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.mainContainer import *


def run():
    cwd = os.getcwd()
    app = QApplication(sys.argv)
    mainWindow = mainContainer()
    # sys.exit(app.exec_())
    app.exec_()
    return

run()
