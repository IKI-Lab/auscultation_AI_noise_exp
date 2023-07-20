import os
import time

import pygame
from moviepy.editor import *
from datetime import date, datetime
from PyQt5 import uic, QtTest
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtCore import QSize, QUrl, QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap, QKeySequence, QTextCursor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QStackedWidget, QWidget, QPushButton, QStyle, QLabel, QAction, QShortcut, QPlainTextEdit

import PostTrial
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h
basedir = os.path.dirname(__file__)
stimuli = os.path.join(basedir, "stimuli")

class Trial(QStackedWidget):
    def __init__(self, exp, trial, widget, test=False, postTrial=False, case=-1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp = exp
        self.widget = widget
        self.test = test
        self.postTrial = postTrial
        self.trial = trial
        self.row = []
        self.mediaPlayer = 0
        self.start = 0
        self.finish = 0
        self.char =""
        if self.postTrial:
            self.build_posttrial_widgets(case)
        else:
            self.build_trial()
            if test:
                self.repeat = RepeatTest()
                self.addWidget(self.repeat)
                self.repeat.again.clicked.connect(self.again)
                self.repeat.start.clicked.connect(self.next)
        # Create exit action on "q"
        self.shortcut = QShortcut(QKeySequence("q"), self)
        self.shortcut.activated.connect(self.handleQuit)

    def build_trial(self):
        self.vignette = Vignette()
        self.vignette.textBrowser.append("<p style=\"font-size:24pt;\">" + self.trial[1] + "</p> ")
        self.addWidget(self.vignette)
        self.setCurrentIndex(0)
        self.vignette.weiterBtn.clicked.connect(self.to_audio)
        self.audio = PlayVideo()
        self.addWidget(self.audio)
        audio = self.trial[2]
        path_a = os.path.join(stimuli, "audio", audio)
        self.audio.pushButton.clicked.connect(lambda: self.play_video(path_a, True))
        self.classification = Classification()
        self.addWidget(self.classification)
        self.classification.ja.clicked.connect(lambda: self.classify(self.classification.positive, self.current() + 1))
        self.classification.nein.clicked.connect(
            lambda: self.classify(self.classification.negative, self.current() + 1))
        self.confidence1 = Confidence()
        self.addWidget(self.confidence1)
        self.add_scale(self.confidence1)
        self.video = PlayVideo()
        self.addWidget(self.video)
        video = self.trial[3]
        path_v = os.path.join(stimuli, "video", video)
        self.video.pushButton.clicked.connect(lambda: self.play_video(path_v))
        self.info = Info()
        self.addWidget(self.info)
        self.info.weiterBtn.clicked.connect(self.next_in_trial)
        self.classification2 = Classification()
        self.addWidget(self.classification2)
        self.classification2.ja.clicked.connect(
            lambda: self.classify(self.classification2.positive, self.current() + 1))
        self.classification2.nein.clicked.connect(
            lambda: self.classify(self.classification2.negative, self.current() + 1))
        self.confidence2 = Confidence()
        self.addWidget(self.confidence2)
        self.add_scale(self.confidence2)
        self.Trust = Trust()
        self.addWidget(self.Trust)
        self.add_scale(self.Trust)
        self.diff = Difficulty()
        self.addWidget(self.diff)
        self.add_scale(self.diff)

    def build_posttrial_widgets(self, case):
        self.case = case
        self.intro = PostTrial.IntroPostTrial(self.exp.group, self.case)
        self.addWidget(self.intro)
        self.intro.weiterBtn.clicked.connect(self.next_in_trial)
        self.setCurrentIndex(0)
        self.vignette = Vignette()
        self.vignette.textBrowser.append("<p style=\"font-size:24pt;\">" + self.trial[1] + "</p> ")
        self.addWidget(self.vignette)
        self.setCurrentIndex(0)
        self.vignette.weiterBtn.clicked.connect(self.to_audio)
        self.video = PlayVideo()
        self.addWidget(self.video)
        video = self.trial[3]
        path_v = os.path.join(stimuli, "video", video)
        self.video.pushButton.clicked.connect(lambda: self.play_video(path_v))
        self.info = Info()
        self.addWidget(self.info)
        self.info.weiterBtn.clicked.connect(self.next_in_trial)
        self.textEdit = PostTrial.OpenPostTrial()
        self.addWidget(self.textEdit)
        self.textEdit.weiterBtn.clicked.connect(self.save_text)
        self.textEdit.plainTextEdit.textChanged.connect(
            lambda: self.handle_text_edit(self.textEdit.plainTextEdit))

    def handleQuit(self):
        if self.mediaPlayer != 0 and self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.stop()
            self.display_info(QMediaPlayer.EndOfMedia)

    def to_audio(self):
        self.row.append(self.trial[0])
        self.next_in_trial()

    def classify(self, value, i):
        if (i == 3 and len(self.row) < 3) or (i == 7 and len(self.row) < 7):
            self.row.append(value)
            self.setCurrentIndex(i)
            self.finish = datetime.now()
            self.row.append((self.finish-self.start).total_seconds())

    def next_in_trial(self):
        self.setCurrentIndex(self.current()+1)


    def play_video(self, full_file_path, audio=False):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(full_file_path)))
        if audio:
            self.mediaPlayer.setVideoOutput(self.audio)
        else:
            self.mediaPlayer.setVideoOutput(self.video)
        self.start = datetime.now()
        # Play
        self.mediaPlayer.play() # with video
        self.mediaPlayer.mediaStatusChanged.connect(self.display_info) # with video
        #self.display_info(QMediaPlayer.EndOfMedia) # video off

    def display_info(self, status):
        if status == QMediaPlayer.EndOfMedia or status == QMediaPlayer.StoppedState:
            self.finish = datetime.now()
            self.row.append((self.finish - self.start).total_seconds())
            trial = self.trial
            values = ["<p style=\"font-size:24pt;\">", "HR: " + str(trial[4]) + '<br>', "AVG Sys: " + str(trial[5])+ '<br>',
                      "AVG Dia: " + str(trial[6])+ '<br>']
            if self.exp.get_group() == "CAA":
                    if trial[-2] == 0:
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
            self.start = datetime.now()

    def add_scale(self, obj):
        obj.pushButton.clicked.connect(lambda: self.measure(1))
        obj.pushButton_2.clicked.connect(lambda: self.measure(2))
        obj.pushButton_3.clicked.connect(lambda: self.measure(3))
        obj.pushButton_4.clicked.connect(lambda: self.measure(4))
        obj.pushButton_5.clicked.connect(lambda: self.measure(5))

    def measure(self, value):
        i = self.current()
        if i == 3 and len(self.row)<5:
            self.row.append(value)
            self.next_in_trial()

        elif (i - len(self.row) == -1):
            self.row.append(value)
            if i == 9 and not self.test and not self.postTrial:
                self.row.append(self.trial[-2])
                self.row.append(self.def_case(self.row[2], self.row[6], self.row[-1]))
                self.exp.data.loc[len(self.exp.data)] = self.row
                self.exp.data.to_csv(basedir + "/files/" + str(self.exp.key) + "_" + str(date.today()) + '.csv', index=False)
                print("saved:")
                print(self.row)
                if self.exp.seqs.iloc[self.exp.key, -1] == self.trial[0]:
                    print("building post-trials...")
                    self.build_post_trial(self.exp)
                self.next()
            else:
                self.next_in_trial()

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
        if len(case) > 0:
            if len(trial) != 0:
                for t, c in zip(trial, case):
                    print("Case:" + str(c) + " Trial: " + str(t[0]) )
                    self.widget.addWidget(Trial(exp, t, self.widget, postTrial=True, case=c))
        self.widget.open_goal = PostTrial.OpenQuestionGoal()
        self.widget.addWidget(self.widget.open_goal)
        self.widget.open_end = PostTrial.OpenQuestion()
        self.widget.addWidget(self.widget.open_end)
        self.widget.end = End()
        self.widget.addWidget(self.widget.end)
        self.widget.open_goal.weiterBtn.clicked.connect(lambda: self.end(1))
        self.widget.open_goal.plainTextEdit.textChanged.connect(
            lambda: self.handle_text_edit(self.widget.open_goal.plainTextEdit))
        self.widget.open_end.weiterBtn.clicked.connect(lambda: self.end(2))
        self.widget.open_end.plainTextEdit.textChanged.connect(
            lambda: self.handle_text_edit(self.widget.open_end.plainTextEdit))

    def handle_text_edit(self, text_edit):
        text = text_edit.toPlainText()
        if (text[:6] == "Tippen"):
            self.char = ""
        if text != "" and bytes(text[-1], 'utf-8') == b'\x08':
            self.char = self.char[:-1]
            text_edit.setPlainText(self.char)
            text_edit.moveCursor(QTextCursor.End)
        if len(text) > 1 and len(text) - len(self.char) > 1:
            if text[-2] == text[-1]:
                self.char = self.char + text[-1]
                text_edit.setPlainText(self.char)
                text_edit.moveCursor(QTextCursor.End)

    def end(self, case):
        self.next()
        if case == 1:
            openq = self.widget.open_goal.plainTextEdit.toPlainText()
        else:
            openq = self.widget.open_end.plainTextEdit.toPlainText()
        with open(basedir + '/files/' + str(self.exp.key) + "_openquestion_" + str(case) + "_" +
                  str(date.today()) + '.txt', 'w+') as f:
            f.write(openq)

    def again(self):
        self.row = []
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

    def save_text(self):
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        openq = self.textEdit.plainTextEdit.toPlainText()
        with open(basedir + '/files/' + str(self.exp.key) +
                                       "_case_" + str(self.case) + "_" + str(date.today()) + '.txt', 'w+') as f:
            f.write(openq)

    def next(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)







class Vignette(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir,'forms/vignette.ui'), self)
        self.textBrowser.setStyleSheet("color:black;")

class VideoPlayer(QMediaPlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
# trial csv
# deleting
# post trial questions
