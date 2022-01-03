import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QPalette, QColor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtCore import QDir, Qt, QUrl
import window

class App(QtWidgets.QMainWindow, window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.media = QMediaPlayer(self)
        self.media.setVideoOutput(self.VideoWidget)
        self.PlayButton.clicked.connect(self.play)
        self.PauseButton.clicked.connect(self.pause)
        self.StopButton.clicked.connect(self.stop)
        self.OpenAction.triggered.connect(self.open)
        self.PlayButton.setEnabled(False)
        self.PauseButton.setEnabled(False)
        self.StopButton.setEnabled(False)
        self.MuteButton.clicked[bool].connect(self.mute)
        self.VolumeSlider.setValue(99)
        self.VolumeSlider.hide()
        self.VolumeButton.clicked[bool].connect(self.ShowVolume)
        self.VolumeSlider.sliderMoved.connect(self.media.setVolume)
        self.TimeSlider.setEnabled(False)
        self.TimeSlider.setRange(0, 0)
        self.TimeSlider.sliderMoved.connect(self.Position)
        self.media.positionChanged.connect(self.positionChanged)
        self.media.durationChanged.connect(self.durationChanged)
        self.FullscreenButton.clicked[bool].connect(self.toggleFullScreen)

        self.Playshortcut = QtWidgets.QShortcut(QKeySequence("Space"), self)
        self.Playshortcut.activated.connect(self.space_play)
        self.Playshortcut.setEnabled(False)

        self.Forwardshortcut = QtWidgets.QShortcut(QKeySequence(QtCore.Qt.Key_Right), self)
        self.Forwardshortcut.activated.connect(self.Forward_play)
        self.Forwardshortcut.setEnabled(False)

        self.Backshortcut = QtWidgets.QShortcut(QKeySequence(QtCore.Qt.Key_Left), self)
        self.Backshortcut.activated.connect(self.Back_play)
        self.Backshortcut.setEnabled(False)

    def Forward_play(self):
        self.media.setPosition(self.media.position() + 5000)

    def Back_play(self):
        self.media.setPosition(self.media.position() - 5000)


    def resizeEvent(self, event):        
        width =  self.size().width()
        height = self.size().height()-20
        self.widget.setGeometry(0, 0, width, height)   

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.menubar.show()
        else:
            self.showFullScreen()
            self.menubar.hide()
            width =  self.size().width()
            height = self.size().height()
            self.widget.setGeometry(0, 0, width, height)
        
    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Выберите видео", '.',
                                                       "Видео файлы (*.mp4 *.flv *.avi)",
                                                       QDir.homePath())
        if fileName != '':
            self.media.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.media.play()
            self.PauseButton.setEnabled(True)
            self.StopButton.setEnabled(True)
            self.TimeSlider.setEnabled(True)
            self.Playshortcut.setEnabled(True)
            self.Forwardshortcut.setEnabled(True)
            self.Backshortcut.setEnabled(True)

    def space_play(self):
        if self.media.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def play(self):
        self.media.play()
        self.PauseButton.setEnabled(True)
        self.PlayButton.setEnabled(False)

    def pause(self):
        self.media.pause()
        self.PlayButton.setEnabled(True)
        self.PauseButton.setEnabled(False)

    def stop(self):
        self.media.stop()
        self.PlayButton.setEnabled(False)
        self.PauseButton.setEnabled(False)
        self.StopButton.setEnabled(False)
        self.TimeSlider.setEnabled(False)
        self.Playshortcut.setEnabled(False)
        self.Forwardshortcut.setEnabled(False)
        self.Backshortcut.setEnabled(False)

    def mute(self, pressed):
        if pressed:
            self.media.setMuted(True)
        else:
            self.media.setMuted(False)

    def ShowVolume(self, pressed):
        if pressed:
            self.VolumeSlider.show()
        else:
            self.VolumeSlider.hide()

    def Position(self, position):
        self.media.setPosition(position)

    def positionChanged(self, position):
        self.TimeSlider.setValue(position)
 
    def durationChanged(self, duration):
        self.TimeSlider.setRange(0, duration)
        
    def Fullscreen(self, pressed):
        if pressed:
            self.VideoWidget.setFullScreen(True)
        else:
            self.VideoWidget.setFullScreen(False)

        

def main():
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    window = App()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()