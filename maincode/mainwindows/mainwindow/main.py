from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon
from maincode.tools.controls import palette


class SGAMain0(QMainWindow):
    def __init__(self, userui):
        super().__init__()
        self.loadui = userui
        self.setObjectName("mainwindow")
        # 窗口大小
        self.resize(910, 580)
        # 窗口名
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # 窗口锁定大小
        self.setFixedSize(self.width(), self.height())
        # 窗口图标
        self.setWindowIcon(QIcon('resources/main/SGA/title.png'))
        self.setPalette(palette)
        self.thread = QThread()
        self.taskthread = None
