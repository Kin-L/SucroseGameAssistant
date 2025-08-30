from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from maincode.tools.constant import spr
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QMovie, QPixmap
from maincode.tools.controls import palette
from sys import argv


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
