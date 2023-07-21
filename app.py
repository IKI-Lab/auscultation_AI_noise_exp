import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PyQt5 import uic, QtWidgets, QtCore
from datetime import date

import PostTrial
from experiment import Experiment
import trial
from welcome import Welcome, KeyDialog, Start
from instructions1 import Instructions1, GroupInstructions, TestStart, postExample

basedir = os.path.dirname(__file__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.exp = Experiment()
        uic.loadUi(os.path.join(basedir,'forms/main_window.ui'), self)
        self.start = Start()
        self.stackedWidget.addWidget(self.start)
        self.stackedWidget.setCurrentIndex(2)
        self.init = False
        self.stackedWidget.tmp = 0

        self.welcome = Welcome()
        self.stackedWidget.addWidget(self.welcome)
        self.instruct = Instructions1(mode="1")
        self.stackedWidget.addWidget(self.instruct)
        self.instruct2 = Instructions1(mode="2")
        self.stackedWidget.addWidget(self.instruct2)
        self.instruct3 = Instructions1(mode="3")
        self.instruct3.textBrowser_2.setStyleSheet("color:black;")
        self.stackedWidget.addWidget(self.instruct3)
        self.instruct_group = GroupInstructions()
        self.stackedWidget.addWidget(self.instruct_group)
        self.test_start = TestStart()
        self.stackedWidget.addWidget(self.test_start)
        self.buildTestTrial()
        self.postexample = postExample()
        self.stackedWidget.addWidget(self.postexample)


        self.start.pushButton_2.clicked.connect(self.openDialog)
        self.welcome.weiterBtn.clicked.connect(self.next)
        self.instruct.weiterBtn.clicked.connect(self.next)
        self.instruct2.weiterBtn.clicked.connect(self.next)
        self.instruct3.weiterBtn.clicked.connect(self.display_instruct_group)
        self.instruct_group.weiterBtn.clicked.connect(self.next)
        self.postexample.weiterBtn.clicked.connect(self.next)
        self.test_start.weiterBtn.clicked.connect(self.next)


    def openDialog(self):
        self.get_key = KeyDialog()
        self.get_key.show()
        self.get_key.pushButton.clicked.connect(self.get_key.accept)
        if self.get_key.exec_() == QtWidgets.QDialog.Accepted:
            self.stackedWidget.setCurrentIndex(self.current() + 1)
        self.initExp()


    def initExp(self):
        key = self.get_key.spinBox.value()
        self.exp.key = key
        self.exp.group = self.exp.set_group(key)
        self.exp.trials_iter = self.exp.get_order()
        self.stackedWidget.tmp = 9 + len(self.exp.trials_iter)  # refactor
        for i in range(len(self.exp.trials_iter)):
            self.buildTrial(self.exp.trials.iloc[self.exp.trials_iter[i], :])
        self.init = True


    def display_instruct_group(self):
        if self.exp.group == "CAA":
            self.instruct_group.textBrowser.append("<p style=\" font-size:24pt; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; color: black; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt font-family:\'Helvetica Neue\'; font-size:18pt;\"><br>Außerdem wird Ihnen die Klassifikation der Auskultation durch das System präsentiert. <br> Diese ist entweder <span style=\" font-weight: bold; color: red;\" > auffällig </span> oder <span style=\"font-weight: bold; color: green ;\" > unauffällig </span>. <br/></span></p> ")
            self.instruct_group.textBrowser.setStyleSheet("font: 50px; color:black;")
        self.stackedWidget.setCurrentIndex(self.current() + 1)


    def buildTestTrial(self):
        trial_test = self.exp.trials.iloc[-1, :]
        self.trialStacked = trial.Trial(self.exp, trial_test, self.stackedWidget, test=True)
        self.stackedWidget.addWidget(self.trialStacked)

    def buildTrial(self, trial_e):
        self.trialStacked = trial.Trial(self.exp, trial_e, self.stackedWidget, test=False)
        self.stackedWidget.addWidget(self.trialStacked)

    def start_post_trial(self):
        self.stackedWidget.setCurrentIndex(self.current() + 1)

    def get_init(self):
        return self.init

    def current(self):
        return self.stackedWidget.currentIndex()
    def next(self):
        self.stackedWidget.setCurrentIndex(self.current() + 1)


if __name__ == '__main__':
    print(QtCore.Qt.Key_Space)
    app = QApplication([])
    window = MainWindow()
    window.showFullScreen()
    app.exec_()




# test if reaction time is correct
# toDo post-trial widget & open questions