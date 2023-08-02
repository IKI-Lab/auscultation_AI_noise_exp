import os
from datetime import date

from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QStackedWidget

from trial import Trial, Vignette, PlayVideo, Info

basedir = os.path.dirname(__file__)
stimuli = os.path.join(basedir, "stimuli")

class IntroPostTrial(QWidget):
        def __init__(self, group, case=0, *args, **kwargs):
            super().__init__(*args, **kwargs)
            path = ""
            if group == "DA":
                path="DA_posttrial.ui"
            else:
                if case == 1:
                    path="CAA_posttrial1.ui"
                else:
                    path="CAA_posttrial2.ui"
            uic.loadUi(os.path.join(basedir, 'forms/'+path), self)
            self.textBrowser.setStyleSheet("color:black;")

class OpenPostTrial(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir, 'forms/' + "open_post_trial.ui"), self)
        self.textBrowser.setStyleSheet("color:black;")

class OpenQuestion(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir, 'forms/' + "open_end.ui"), self)
        self.textBrowser.setStyleSheet("color:black;")

class OpenQuestionGoal(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir, 'forms/' + "open_goal.ui"), self)
        self.textBrowser.setStyleSheet("color:black;")