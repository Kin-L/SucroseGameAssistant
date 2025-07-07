from maincode.tools.controls import (Line, Stack, Widget,
                                     PicButton, InfoBox, OverallButton,
                                     tips, Support)
from sys import argv
from ctypes import windll


class MainWidget(Widget):
    def __init__(self):
        super().__init__()
        self.sksetting = Stack(self, (5, 0, 625, 575))
        Line(self, (5, 38, 625, 3))
        # 全局/模块 设置按钮
        self.btsetting = OverallButton(self)
        if "showconsole" in argv:
            self.console_window = windll.kernel32.GetConsoleWindow()
        self.obstate = False
        self.obconsole = True
        self.support = Support()
        # 历史信息按钮
        historypath = r"resources/main/button/history.png"
        savepath = r"resources/main/button/save.png"
        sizetp = (25, 25)
        self.bthistory = PicButton(self, (555, 0, 35, 35), historypath, sizetp)
        self.btconfigsave = PicButton(self, (515, 0, 35, 35), savepath, sizetp)
        tips(self.btconfigsave, "手动保存当前页面和全局设置,并应用定时(快捷键：ctrl+s)")
        # 指示信息窗口
        self.infobox = InfoBox(self)

    def changeob(self):
        if self.obstate:
            self.sksetting.setCurrentIndex(1)
            self.obstate = False
        else:
            self.sksetting.setCurrentIndex(0)
            self.obstate = True

    def changecs(self):
        if self.obconsole:
            windll.user32.ShowWindow(self.console_window, 0)
            self.obconsole = False
        else:
            windll.user32.ShowWindow(self.console_window, 1)
            self.obconsole = True
