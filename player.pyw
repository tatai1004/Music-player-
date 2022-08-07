#! /usr/bin/env python3

from functools import partial
import sys
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, \
    QFrame, QGraphicsDropShadowEffect, QGraphicsView, QGraphicsScene, QLabel, \
    QPushButton, QHBoxLayout, QStyle, QListWidget, QFileDialog
from PyQt5.QtGui import QGradient, QFont, QColor, QCursor, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Love By Chance Developed by Tatai')

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)
        self.url = QUrl()

        # Setup the container
        container = QGridLayout()

        # Add the widgets
        container.addWidget(self._header(), 0, 0, 1, 3)
        container.addWidget(self._status(), 1, 0, 1, 1)
        container.addWidget(self._track(), 1, 1, 1, 1)
        container.addWidget(self._button(), 1, 2, 1, 1)
        container.addWidget(self._left(), 2, 0, 2, 1)
        container.addWidget(self._right(), 2, 1, 1, 2)
        container.addLayout(self._buttons(), 3, 1, 1, 2)
        container.addWidget(self._footer(), 4, 0, 1, 3)

        widget = QWidget()
        widget.setLayout(container)
        self.setCentralWidget(widget)

        self.playlist.currentIndexChanged.connect(partial(self._update_index))

    def _header(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(3)
        shadow.setOffset(3, 3)

        scene = QGraphicsScene()

        view = QGraphicsView()
        view.setMinimumSize(800, 100)
        view.setMaximumHeight(100)
        view.setScene(scene)

        gradient = QGradient(QGradient.RichMetal)

        scene.setBackgroundBrush(gradient)

        font = QFont('comic sans ms', 40, QFont.Bold)

        text = scene.addText('Love By Chance')
        text.setDefaultTextColor(QColor(250, 250, 250))
        text.setFont(font)

        text.setGraphicsEffect(shadow)

        return view

    def _update_index(self):
        self.music_list.setCurrentRow(self.playlist.currentIndex())
        if self.playlist.currentIndex() < 0:
            self.music_list.setCurrentRow(0)

    def _status(self):
        self.status = QLabel('Status: Stopped')
        self.status.setFrameShape(QFrame.Box)
        self.status.setFrameShadow(QFrame.Sunken)
        self.status.setStyleSheet('padding: 5px')
        self.status.setMaximumHeight(40)
        return self.status

    def _track(self):
        self.track = QLabel('Track: No track is playing')
        self.track.setFrameShape(QFrame.Box)
        self.track.setFrameShadow(QFrame.Sunken)
        self.track.setStyleSheet('padding: 5px')
        self.track.setMaximumHeight(40)
        return self.track

    def _button(self):
        button = QPushButton('Open Folder')
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.released.connect(self._get_files)
        button.setStyleSheet('''
        QPushButton{border: 1px solid gray; padding: 5px; border-style: outset;
        background-color: silver;}
        QPushButton:hover{ background-color: lightgray; padding: 5px;
        border-style: outset; border: 1px solid gray; font-weight: bold;}
        QPushButton:pressed {border: 2px solid gray; padding: 5px;
        background-color: silver; border-style: inset; font-weight: bold;}
        ''')
        return button

    def _get_files(self):
        files = QFileDialog.getOpenFileNames(
            None, 'Audio File Formats', filter='(*.mp3 *.wav *.ogg *.mpeg)')
        for file in files[0]:
            self.playlist.addMedia(QMediaContent(self.url.fromLocalFile(file)))
            file = file.split('/')
            self.music_list.addItem(str(file[-1][:-4]))
        self.music_list.setCurrentRow(0)
        self.playlist.setCurrentIndex(0)

    def _left(self):
        frame = QFrame()
        frame.setFrameShape(frame.Box)
        frame.setFrameShadow(frame.Sunken)
        frame.setMinimumHeight(300)
        return frame

    def _right(self):
        self.music_list = QListWidget()
        self.music_list.setFrameShape(QFrame.Box)
        self.music_list.setFrameShadow(QFrame.Sunken)
        self.music_list.setStyleSheet('background-color: snow;')
        return self.music_list

    def _exit(self):
        sys.exit()

    def _buttons(self):

        layout = QHBoxLayout()
        buttons = {
            'Play': partial(self._command, action='play'), 'Stop': partial(self._command, action='stop'),
            'Next': partial(self._command, action='next'), 'Prev': partial(self._command, action='prev'),
            'Clear List': partial(self._command, action='clear'), 'Exit': partial(self._exit)
        }

        for button, cmd in buttons.items():
            btn = QPushButton(button)
            btn.setCursor(Qt.PointingHandCursor)
            btn.released.connect(cmd)
            if button == 'Exit':
                btn.setStyleSheet('''
                QPushButton{background-color: firebrick; color: black;}
                QPushButton:hover{background-color: tomato; color: red;
                font-weight: bold;}
                QPushButton:pressed{background-color: red; color: white; font-weight: normal;}
                ''')
            elif button == 'Clear List':
                btn.setStyleSheet('''
                                  QPushButton{background-color: darkorange;}
                                  QPushButton:hover{background-color: orange; color: red; font-weight: bold;}
                                  ''')
            else:
                btn.setStyleSheet('''
                QPushButton{background-color: skyblue;}
                QPushButton:hover{background-color: lightskyblue; font-weight: bold;}
                QPushButton:pressed{background-color: dodgerblue; font-weight: bold;}
                ''')
            layout.addWidget(btn)

        return layout

    def _command(self, action=None):
        if action == 'play':
            self.player.play()
        elif action == 'stop':
            self.player.stop()
        elif action == 'next':
            self.playlist.next()
            self.player.play()
        elif action == 'prev':
            self.playlist.previous()
            self.player.play()
        elif action == 'clear':
            self.music_list.clear()
            self.player.stop()
            self.playlist.clear()
        self.playlist.setCurrentIndex(0)
        self.music_list.setCurrentRow(self.playlist.currentIndex())

        if action == 'stop' or action == 'clear':
            self.status.setText('Status: Stopped')
        else:
            if self.music_list.currentItem():
                self.track.setText(
                    f'Track: {self.music_list.currentItem().text().title()}')
                self.status.setText('Status: Now Playing')
            else:
                pass

    def _footer(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(3)
        shadow.setOffset(3, 3)

        scene = QGraphicsScene()

        view = QGraphicsView()
        view.setMinimumSize(800, 40)
        view.setMaximumHeight(40)
        view.setScene(scene)

        gradient = QGradient(QGradient.RichMetal)

        scene.setBackgroundBrush(gradient)

        font = QFont('comic sans ms', 10, QFont.Bold)

        text = scene.addText('dev by - 15/05/2022')
        text.setDefaultTextColor(QColor(250, 250, 250))
        text.setFont(font)

        text.setGraphicsEffect(shadow)

        return view


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


main()
