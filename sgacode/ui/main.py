from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor, QMovie, QPixmap
from sgacode.tools.main import env, GetHwnd
from sys import argv
from typing import Optional
from sgacode.ui.control import (Line, Stack, Widget,
                                PicButton, InfoBox, OverallButton)
from sgacode.ui.overall.main import OverallWindow
from sgacode.ui.module.main import ModuleWindow
from sgacode.ui.module.moduleclass import SGAModuleGroup
from sgacode.configclass import SGAMainConfig


class SGAMainWindow(Widget):
    def __init__(self):
        super().__init__()
        self.sksetting = Stack(self, (5, 0, 625, 575))
        # 指示图标
        # waitpath = r"resources/main/button/state/wait.png"
        # self.picstate = Picture((485, 430, 150, 150), waitpath)
        Line(self, (5, 38, 625, 3))
        # 全局/模块 设置按钮
        self.btsetting = OverallButton(self)
        # 历史信息按钮
        historypath = r"resources/main/button/history.png"
        savepath = r"resources/main/button/save.png"
        sizetp = (25, 25)
        self.bthistory = PicButton(self, (555, 0, 35, 35), historypath, sizetp)
        self.btconfigsave = PicButton(self, (515, 0, 35, 35), savepath, sizetp)
        # 指示信息窗口
        self.infobox = InfoBox(self)
        self.overall: Optional[OverallWindow] = None
        self.module: Optional[ModuleWindow] = None

    def LoadMainSet(self, smc: SGAMainConfig):
        # 全局设置窗口
        self.overall = OverallWindow(smc)
        self.sksetting.addWidget(self.overall)

    def LoadSubSet(self, smc: SGAMainConfig, smg: SGAModuleGroup):
        # # 模组设置窗口
        self.module = ModuleWindow(smc, smg)
        self.sksetting.addWidget(self.module)
        self.sksetting.setCurrentIndex(1)
        self.module.SubModuleInit()


class SGAQMainWindow(QMainWindow):
    def __init__(self, thread):
        super().__init__()
        self.thread = thread
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
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)
        # 加载动画，置顶窗口，等待SGA加载完成后再取消
        self.loading = LoadWindow(self)
        self.loading.raise_()
        self.loading.lower()
        self.SMW: Optional[SGAMainWindow] = None
        # 窗口显现
        self.show()
        env.hwnd = GetHwnd(True, "Qt5152QWindowIcon", "砂糖代理")
        if len(argv) <= 1:
            env.foreground()
        elif argv[1] != "True":
            env.foreground()

    def LoadMainWindows(self) -> SGAMainWindow:
        self.SMW = SGAMainWindow()
        self.setCentralWidget(self.SMW)  # 关键步骤！
        return self.SMW

    def closeEvent(self, event):
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        super().closeEvent(event)


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
