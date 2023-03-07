import os

from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QDialog

basedir = os.path.dirname(__file__)


class Welcome(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/welcome.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")
        self.weiterBtn.setStyleSheet("background-color: blue; font: bold 30px; color: white;")

class Start(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/start.ui'), self)

class KeyDialog(QDialog):
    def __init__(self):
        super(KeyDialog, self).__init__()
        uic.loadUi(os.path.join(basedir,'forms/key.ui'), self)
        self.enterLabel.setStyleSheet("color:black;")
        self.spinBox.setStyleSheet("color:black;")

