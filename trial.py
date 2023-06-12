import os
import time

import pygame
from moviepy.editor import *
from datetime import date, datetime
from PyQt5 import uic, QtTest
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize, QUrl, QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QStackedWidget, QWidget, QPushButton, QStyle, QLabel
from PyQt5 import QtCore, QtWidgets

import PostTrial
from instructions1 import TestStart
from pygame import mixer
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h



basedir = os.path.dirname(__file__)
stimuli = os.path.join(basedir, "stimuli")
class Trial(QStackedWidget):
    def __init__(self, exp, trial, widget, test=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp = exp
        self.row = []
        self.widget = widget
        self.test = test
        self.trial = trial
        self.start = 0
        self.finish = 0
        self.vignette = Vignette()
        print(self.trial[1])
        self.vignette.textBrowser.append("<p style=\"font-size:24pt;\">" + self.trial[1] + "</p> ")

        self.addWidget(self.vignette)
        self.setCurrentIndex(0)
        self.vignette.weiterBtn.clicked.connect(self.to_audio)
        self.play_audio = PlayAudio()
        self.player = QMediaPlayer()
        self.addWidget(self.play_audio)
        self.play_audio.pushButton.clicked.connect(self.play_sound)

        self.classification = Classification()
        self.addWidget(self.classification)
        self.classification.ja.clicked.connect(lambda: self.classify(self.classification.positive,
                                                                     self.currentIndex() + 1))
        self.classification.nein.clicked.connect(lambda: self.classify(self.classification.negative,
                                                                       self.currentIndex() + 1))

        self.confidence1 = Confidence()
        self.addWidget(self.confidence1)
        self.add_scale(self.confidence1)

        self.video = PlayVideo()
        self.addWidget(self.video)
        self.video.pushButton.clicked.connect(self.play_video)

        self.info = Info()
        self.addWidget(self.info)
        self.info.weiterBtn.clicked.connect(self.classify_after)

        self.classification2 = Classification()
        self.addWidget(self.classification2)
        self.classification2.ja.clicked.connect(lambda: self.classify(self.classification2.positive,
                                                                      self.currentIndex() + 1))
        self.classification2.nein.clicked.connect(lambda: self.classify(self.classification2.negative,
                                                                        self.currentIndex() + 1))


        self.confidence2 = Confidence()
        self.addWidget(self.confidence2)
        self.add_scale(self.confidence2)

        self.Trust = Trust()
        self.addWidget(self.Trust)
        self.add_scale(self.Trust)

        self.Use = Use()
        self.addWidget(self.Use)
        self.add_scale(self.Use)

        self.diff = Difficulty()
        self.addWidget(self.diff)
        self.add_scale(self.diff)

        if test:
            self.repeat = RepeatTest()
            self.addWidget(self.repeat)
            self.repeat.again.clicked.connect(self.again)
            self.repeat.start.clicked.connect(self.next)



    def to_audio(self):
        self.row.append(self.trial[0])
        self.setCurrentIndex(self.current()+1)

    def play_sound(self):
        audio = self.trial[2]
        full_file_path = os.path.join(stimuli, "audio" ,audio)
        mixer.init()
        record = mixer.Sound(full_file_path)
        len_rec = int(record.get_length())
        ##mixer.Sound.play(record) #dev
        ##mixer.music.stop() #dev
        #time.sleep(len_rec+2) #dev
        print(self.row)
        self.setCurrentIndex(self.current()+1)
        self.start = datetime.now()

    def classify(self, value, i):
        if (i == 3 and len(self.row) < 2) or (i == 7 and len(self.row) < 5):
            self.row.append(value)
            print(self.row)
            self.setCurrentIndex(i)
            self.finish = datetime.now()
            self.row.append((self.finish-self.start).total_seconds())

    def classify_after(self):
        self.setCurrentIndex(self.current()+1)


    def play_video(self):
        video = self.trial[3]
        full_file_path = os.path.join(stimuli, "video", video)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        print(full_file_path)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(full_file_path)))
        self.mediaPlayer.setVideoOutput(self.video)
        # Play
        #self.mediaPlayer.play() # with video
        #self.mediaPlayer.mediaStatusChanged.connect(self.display_info) # with video
        self.display_info(QMediaPlayer.EndOfMedia) # video off

    def display_info(self, status):
        if status == QMediaPlayer.EndOfMedia:
            trial = self.trial
            values = ["<p style=\"font-size:24pt;\">", "HR: " + str(trial[4]) + '<br>', "AVG Sys: " + str(trial[6])+ '<br>',
                      "AVG Dia: " + str(trial[7])+ '<br>']

            print(self.exp.get_group())
            if self.exp.get_group() == "CAA":
                    if trial[8] == 0:
                        pred = "<span style=\"font-weight: bold; color: green ;\" > unauffällig </span></p>"
                    else:
                        pred = "<span style=\"font-weight: bold; color: red ;\" > auffällig </span></p>"
                    values.append("Einschätzung des Systems: " + pred)
            values = "<br>".join(values)
            self.info.textBrowser.setHtml(values)
            self.info.textBrowser.setStyleSheet("color:black;")
            self.info.textBrowser.setFixedHeight(400)
            self.info.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.info.textBrowser.setAlignment(Qt.AlignCenter)
            self.setCurrentIndex(self.current() + 1)

    def add_scale(self, obj):
        obj.pushButton.clicked.connect(lambda: self.measure(1, self.currentIndex() + 1))
        obj.pushButton_2.clicked.connect(lambda: self.measure(2, self.currentIndex() + 1))
        obj.pushButton_3.clicked.connect(lambda: self.measure(3, self.currentIndex() + 1))
        obj.pushButton_4.clicked.connect(lambda: self.measure(4, self.currentIndex() + 1))
        obj.pushButton_5.clicked.connect(lambda: self.measure(5, self.currentIndex() + 1))

    def measure(self, value, i):
        if i == 4 and len(self.row)<4:
            self.row.append(value)
            self.setCurrentIndex(i)

        elif (i - len(self.row) == 2):
            self.row.append(value)
            self.setCurrentIndex(i)


        if i == 11 and not self.test:
            self.row.append(self.trial[8])
            # case
            self.row.append(self.def_case(self.row[1], self.row[4], self.row[-1]))
            self.exp.data.loc[len(self.exp.data)] = self.row
            self.exp.data.to_csv(basedir + "/files/" + str(self.exp.key) + "_" + str(date.today()) + '.csv', index=False)
            if self.widget.tmp == self.widget.currentIndex():
                self.build_post_trial(self.exp)
            else:
                self.next()

    def build_post_trial(self, exp):
        trial = []
        case = []
        self.widget.wait = Wait()
        self.widget.addWidget(self.widget.wait)
        self.widget.wait.pushButton.clicked.connect(self.next)
        if exp.group == "CAA":
            case1 = exp.data[exp.data["case"] == 1]
            if len(case1) > 0:
                seq = case1.iloc[0, 0]
                trial = [exp.trials[exp.trials["seq"] == seq].iloc[0, :]]
                case = [1]

            case2 = exp.data[exp.data["case"] == 2]
            if len(case2) > 0:
                seq = case2.iloc[0, 0]
                trial.append(exp.trials[exp.trials["seq"] == seq].iloc[0, :])
                case.append(2)


        else:
            case = exp.data[exp.data["case"] == 1]
            if len(case) > 0:
                seq = case.iloc[0, 0]
                trial = [exp.trials[exp.trials["seq"] == seq].iloc[0, :]]
                case = [1]
        print(len(trial))
        if len(case) > 0:
            if len(trial) != 0:
                for t, c in zip(trial, case):
                    self.widget.posttrialStacked = PostTrial.PostTrial(exp, c, t, self.widget)
                    self.widget.addWidget(self.widget.posttrialStacked)
        self.widget.open_goal = PostTrial.OpenQuestionGoal()
        self.widget.addWidget(self.widget.open_goal)
        self.widget.open_end = PostTrial.OpenQuestion()
        self.widget.addWidget(self.widget.open_end)
        self.widget.end = End()
        self.widget.addWidget(self.widget.end)
        self.widget.open_goal.weiterBtn.clicked.connect(lambda: self.end(1))
        self.widget.open_end.weiterBtn.clicked.connect(self.end)
        self.next()


    def end(self, case=2):
        self.next()
        openq = self.widget.open_end.plainTextEdit.toPlainText()
        with open(basedir + '/files/' + str(self.exp.key) + "_openquestion_" + str(case) + "_" +
                  str(date.today()) + '.txt', 'w+') as f:
            f.write(openq)

    def again(self):
        self.row = []
        print(self.row)
        self.setCurrentIndex(0)

    def get_results(self):
        return self.row

    def current(self):
        return self.currentIndex()

    def def_case(self, res1, res2, pred):
        if self.exp.group == "CAA":
            if (res1 == 0 and res2 == 0 and pred == 1) or (res1 == 1 and res2 == 1 and pred == 0):
                return 1
            elif (res1 == 1 and res2 == 0 and pred == 0) or (res1 == 0 and res2 == 1 and pred == 1):
                return 2
            else:
                return 0
        else:
            if (res1 == 0 and res2 == 1) or (res1 == 1 and res2 == 0):
                return 1
            else:
                return 0

    def next(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)







class Vignette(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/vignette.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")

class PlayAudio(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/play_audio.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")
        self.pushButton.setStyleSheet("background-color: blue; font: bold 30px; color: white;")
        self.pushButton.setIconSize(QSize(50, 50))

class Classification(QWidget):
    positive = 1
    negative = 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/classify.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")


class PlayVideo(QVideoWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/play_video.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")
        self.pushButton.setStyleSheet("background-color: blue; font: bold 30px; color: white;")
        self.pushButton.setIconSize(QSize(50, 50))

class Info(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir, 'forms/welcome.ui'), self)
        #self.textBrowser.setHtml("")
        #self.textBrowser.hide()
        self.weiterBtn.setStyleSheet("background-color: blue; font: bold 30px; color: white;")


class Confidence(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/confidence.ui'), self)

class Trust(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/trust.ui'), self)

class Use(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/use.ui'), self)

class Difficulty(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/diff.ui'), self)



class End(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir, 'forms/welcome.ui'), self)
        self.textBrowser.setHtml("")
        self.textBrowser.hide()
        self.weiterBtn.hide()
        self.info_label = QLabel("Vielen Dank für Ihre Teilnahme!", self)
        self.info_label.setStyleSheet("font-size: 50pt; color:black")
        self.info_label.move(int(self.width() * 0.3), int(self.height() * 0.5))
        self.info_label.setAlignment(Qt.AlignCenter)

class Wait(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/wait.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")


class RepeatTest(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/repeat_test.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")

# change mouse position
# media player alternative
# certainty
