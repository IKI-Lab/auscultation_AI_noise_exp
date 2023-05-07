import os
from datetime import date

from PyQt6 import uic
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QWidget, QStackedWidget

from trial import Vignette, PlayVideo, Info

basedir = os.path.dirname(__file__)
stimuli = os.path.join(basedir, "stimuli")
class PostTrial(QStackedWidget):
    def __init__(self, exp, case, trial, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp = exp
        self.case = case
        self.trial = trial
        self.widget = widget

        self.intro = self.set_intro()
        self.addWidget(self.intro)
        self.intro.weiterBtn.clicked.connect(self.next)
        self.setCurrentIndex(0)

        self.vignette = Vignette()
        self.vignette.textBrowser.append("<p style=\"font-size:24pt;\">" + self.trial[1] + "</p> ")
        self.addWidget(self.vignette)
        self.vignette.weiterBtn.clicked.connect(self.next)

        self.video = PlayVideo()
        self.addWidget(self.video)
        self.video.pushButton.clicked.connect(self.play_video)

        self.info = Info()
        self.addWidget(self.info)
        self.info.weiterBtn.clicked.connect(self.next)

        self.textEdit = OpenPostTrial()
        self.addWidget(self.textEdit)
        self.textEdit.weiterBtn.clicked.connect(self.save_text)



    def play_video(self):
            video = self.trial[3]
            full_file_path = os.path.join(stimuli, "video", video)
            self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            print(full_file_path)
            # self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(full_file_path)))
            # self.mediaPlayer.setVideoOutput(self.video)
            # Play
            # self.mediaPlayer.play()
            # self.mediaPlayer.mediaStatusChanged.connect(self.display_info)
            self.display_info(QMediaPlayer.EndOfMedia)  # for dev mode

    def display_info(self, status):
            if status == QMediaPlayer.EndOfMedia:
                # Creates the QLabel 'background' which will contain the white background
                trial = self.trial
                # Creates a blank version of the chosen word
                values = ["HR: " + str(trial[4]), "AVG Sys: " + str(trial[6]),
                          "AVG Dia: " + str(trial[7])]

                print(self.exp.get_group())
                if self.exp.get_group() == "CAA":
                    if trial[8] == 0:
                        pred = "unauffällig"
                    else:
                        pred = "auffällig"
                    values.append("Prediction: " + pred)
                values = "\n".join(values)
                self.info.info_label.setText(values)
                self.setCurrentIndex(self.current() + 1)


    def set_intro(self):
        return IntroPostTrial(self.exp.group, self.case)
    def next(self):
        self.setCurrentIndex(self.current()+1)
    def current(self):
        return self.currentIndex()

    def save_text(self):
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        openq = self.textEdit.plainTextEdit.toPlainText()
        with open(basedir + '/files/' + str(self.exp.key) +
                                       "_case_" + str(self.case) + "_" + str(date.today()) + '.txt', 'w+') as f:
            f.write(openq)

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
        self.plainTextEdit.setStyleSheet("color:black;")

class OpenQuestion(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(basedir, 'forms/' + "open_end.ui"), self)
        self.textBrowser.setStyleSheet("color:black;")
        self.plainTextEdit.setStyleSheet("color:black;")