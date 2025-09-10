from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QShortcut
from maincode.tools.core.constant import spr
from maincode.tools.sgaqt.widgets import palette
from sys import argv
from maincode.mainwindows.mainwidget import MainWidget
from maincode.config.configctrl import scc
from maincode.tools.controller.ocr import OCR
import os
from pathlib import Path as libPath
from maincode.tools.core.logger import logger
from maincode.tools.system.notification import GetTracebackInfo


class SGAQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("mainwindow")
        self.resize(910, 580)
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(spr.SGATitlePic))
        self.setPalette(palette)
        self.SG = scc
        self.OCR = OCR
        self.loading = None  # 防止未初始化访问
        self.timer = QTimer(self)
        self.quicksave = QShortcut("Ctrl+S", self)
        self.sleeptime = 0
        self.timerallow = True
        self.infoHead = logger.infoHead
        self.infoAdd = logger.infoAdd
        self.infoEnd = logger.infoEnd

    def _init_loading_ui(self):
        self.loading = LoadWidget(self)
        self.show()

        from maincode.tools.system.window import GetWindow
        self.window = GetWindow("砂糖代理")
        if "back" not in argv:
            self.window.foreground()

        self.mainwidget = MainWidget()
        self.setCentralWidget(self.mainwidget)

        self.infoHead = self.mainwidget.infoHead
        self.infoAdd = self.mainwidget.infoAdd
        self.infoEnd = self.mainwidget.infoEnd

        self.mainwidget.btconsole.toggled.connect(self.mainwidget.changecs)
        self.mainwidget.btsetting.toggled.connect(self.mainwidget.changeob)
        for i in self.SG.loadstate.items():
            if i[1]:
                self.mainwidget.infoAdd(i[0], False)
        self.mainwidget.bthistory.clicked.connect(self._open_history)

    def _open_history(self):
        try:
            latest_file = max(
                [f for f in libPath(spr.LogsDir).iterdir() if f.is_file()],
                key=lambda f: f.stat().st_ctime
            )
            os.startfile(str(latest_file))
        except Exception as e:
            self.infoHead()
            self.infoAdd("打开历史日志异常")
            self.infoEnd()
            logger.error(GetTracebackInfo(e)+"打开历史日志异常")


class LoadWidget(QWidget):
    def __init__(self, _widget: QMainWindow):
        super().__init__(_widget)
        self.setGeometry(0, 0, 910, 580)
        self.setPalette(palette)

        self.loadbacklab = QLabel("", self)
        self.loadbacklab.setPixmap(QPixmap(spr.LoadBackPic))
        self.loadbacklab.setGeometry(0, 0, 910, 580)
        self.loadbacklab.setScaledContents(True)

        self.loadgiflab = QLabel("", self)
        self.loadgifmov = QMovie(spr.LoadingGif)
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
