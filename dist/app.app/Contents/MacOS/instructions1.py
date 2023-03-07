import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

basedir = os.path.dirname(__file__)

class Instructions1(QWidget):
    def __init__(self, mode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/instructions' + mode +'.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")
        #self.weiterBtn.setStyleSheet("background-color: blue; font: bold 30px; color: white;")


class GroupInstructions(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/group_instruct.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")


class TestStart(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/test_start.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")

class postExample(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/postExample.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")