from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from maincode.tools.constant import spr
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QShortcut
from PyQt5.QtGui import QMovie, QPixmap
from maincode.tools.controls import palette
from sys import argv
from maincode.mainwindows.mainwidget import MainWidget
from maincode.config.maingroup import sg
import os
from pathlib import Path as libPath


class SGAQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("mainwindow")
        # 窗口大小
        self.resize(910, 580)
        # 窗口名
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # 窗口锁定大小
        self.setFixedSize(self.width(), self.height())
        # 窗口图标
        self.setWindowIcon(QIcon(spr["SGATitlePic"]))
        self.setPalette(palette)
        if spr["LoadUI"]:
            self.loading = LoadWidget(self)
            self.show()
            # 窗口显现
            from maincode.tools.main import GetWindow
            self.window = GetWindow("砂糖代理")
            if "back" not in argv:
                self.window.foreground()
            self.mainwidget = MainWidget()
            self.setCentralWidget(self.mainwidget)

            sg.infoHead.connect(self.mainwidget.infoHead)
            sg.infoAdd.connect(self.mainwidget.infoAdd)
            sg.infoEnd.connect(self.mainwidget.infoEnd)
            self.infoHead = self.mainwidget.infoHead
            self.infoAdd = self.mainwidget.infoAdd
            self.infoEnd = self.mainwidget.infoEnd
        if spr["ShowConsole"]:
            self.mainwidget.btconsole.toggled.connect(self.mainwidget.changecs)
        self.mainwidget.btsetting.toggled.connect(self.mainwidget.changeob)
        self.mainwidget.bthistory.clicked.connect(lambda: os.startfile(
            max([f for f in libPath(spr["LogsDir"]).iterdir() if f.is_file()],
                key=lambda f: f.stat().st_ctime)))
        self.sleeptime = 0
        self.timerallow = True
        self.quicksave = QShortcut("Ctrl+S", self)
        self.timer = QTimer(self)


class LoadWidget(QWidget):
    def __init__(self, _widget: QMainWindow):
        super().__init__(_widget)
        self.setGeometry(0, 0, 910, 580)
        self.setPalette(palette)

        self.loadbacklab = QLabel("", self)
        self.loadbacklab.setPixmap(QPixmap(spr["LoadBackPic"]))
        self.loadbacklab.setGeometry(0, 0, 910, 580)
        self.loadbacklab.setScaledContents(True)

        self.loadgiflab = QLabel("", self)
        self.loadgifmov = QMovie(spr["LoadingGif"])
        self.loadgiflab.setMovie(self.loadgifmov)
        self.loadgiflab.setGeometry(430, 440, 50, 50)
        self.loadgiflab.setScaledContents(True)
        self.loadgifmov.start()
        self.raise_()
