from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPalette, QColor, QMovie, QPixmap


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
        self.setWindowIcon(QIcon('resources/main/SGA/icon.png'))
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)
        # 加载动画，置顶窗口，等待SGA加载完成后再取消
        self.loading = LoadWindow(self)
        self.loading.raise_()
        # self.loading.lower()


class LoadWindow(QWidget):
    def __init__(self, _widget):
        super().__init__(_widget)
        self.setGeometry(0, 0, 910, 580)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)

        backpath = r'resources/main/SGA/loadback.png'
        self.loadbacklab = QLabel("", self)
        self.loadbacklab.setPixmap(QPixmap(backpath))
        self.loadbacklab.setGeometry(0, 0, 910, 580)
        self.loadbacklab.setScaledContents(True)

        loadgifpath = r'resources/main/SGA/loading.gif'
        self.loadgiflab = QLabel("", self)
        self.loadgifmov = QMovie(loadgifpath)
        self.loadgiflab.setMovie(self.loadgifmov)
        self.loadgiflab.setGeometry(430, 440, 50, 50)
        self.loadgiflab.setScaledContents(True)
        self.loadgifmov.start()
