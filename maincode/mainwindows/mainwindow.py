from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QShortcut

import maincode.tools.system.window
from maincode.tools.core.constant import spr
from maincode.tools.sgaqt.widgets import palette
from sys import argv
from maincode.mainwindows.mainwidget import MainWidget
from maincode.config.configctrl import scc
from maincode.tools.controller.ocr import OCR
import os
from pathlib import Path as libPath


class SGAQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("mainwindow")
        self.resize(910, 580)
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(spr["SGATitlePic"]))
        self.setPalette(palette)
        self.SG = scc
        self.OCR = OCR
        self.loading = None  # 防止未初始化访问
        self.timer = QTimer(self)
        self.quicksave = QShortcut("Ctrl+S", self)

        if spr["LoadUI"]:
            self._init_loading_ui()

        self.sleeptime = 0
        self.timerallow = True

    def _init_loading_ui(self):
        self.loading = LoadWidget(self)
        self.show()

        from maincode.tools.system.window import GetWindow
        self.window = GetWindow("砂糖代理")
        if "back" not in argv:
            maincode.tools.system.window.foreground()

        self.mainwidget = MainWidget()
        self.setCentralWidget(self.mainwidget)

        self.SG.infoHead.connect(self.mainwidget.infoHead)
        self.SG.infoAdd.connect(self.mainwidget.infoAdd)
        self.SG.infoEnd.connect(self.mainwidget.infoEnd)
        self.infoHead = self.mainwidget.infoHead
        self.infoAdd = self.mainwidget.infoAdd
        self.infoEnd = self.mainwidget.infoEnd

        if spr["ShowConsole"]:
            self.mainwidget.btconsole.toggled.connect(self.mainwidget.changecs)
        self.mainwidget.btsetting.toggled.connect(self.mainwidget.changeob)

        logs_dir = spr["LogsDir"]
        if os.path.exists(logs_dir):
            try:
                latest_file = max(
                    [f for f in libPath(logs_dir).iterdir() if f.is_file()],
                    key=lambda f: f.stat().st_ctime
                )
                self.mainwidget.bthistory.clicked.connect(lambda: os.startfile(str(latest_file)))
            except ValueError:
                # 目录为空时忽略
                pass


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

    def closeEvent(self, event):
        # 确保资源释放
        if self.loadgifmov:
            self.loadgifmov.stop()
        super().closeEvent(event)
