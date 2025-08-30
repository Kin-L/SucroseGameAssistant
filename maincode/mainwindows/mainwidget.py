from maincode.tools.controls import (Line, Stack, Widget,
                                     PicButton, InfoBox, OverallButton,
                                     tips, Support, ConsoleButton)
from ctypes import windll
from maincode.tools.constant import spr
import os
from pathlib import Path as libPath
from time import localtime, strftime
from maincode.tools.main import logger


class MainWidget(Widget):
    def __init__(self):
        super().__init__()
        self.sksetting = Stack(self, (5, 0, 625, 575))
        Line(self, (5, 38, 625, 3))
        # 全局/模块 设置按钮
        self.btsetting = OverallButton(self)
        if spr["ShowConsole"]:
            self.console_window = windll.kernel32.GetConsoleWindow()
        self.obstate = False
        self.obconsole = True
        self.support = Support()
        # 历史信息按钮
        sizetp = (25, 25)
        self.bthistory = PicButton(self, (555, 0, 35, 35), spr["SGATitlePic"], sizetp)
        self.btconfigsave = PicButton(self, (515, 0, 35, 35), spr["SavePic"], sizetp)
        tips(self.btconfigsave, "手动保存并应用当前页面设置(快捷键：ctrl+s)")
        # 指示信息窗口
        self.infobox = InfoBox(self)

        if spr["ShowConsole"]:
            self.btconsole = ConsoleButton(self)
            self.btconsole.setChecked(True)
            self.btconsole.toggled.connect(self.changecs)
        self.btsetting.toggled.connect(self.changeob)
        self.bthistory.clicked.connect(lambda: os.startfile(
            max([f for f in libPath(spr["LogsDir"]).iterdir() if f.is_file()],
                key=lambda f: f.stat().st_ctime)))

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
    
    def infoAdd(self, msg: str = "", addtime=True):
        if addtime:
            timestr = strftime("%H:%M:%S ", localtime())
        else:
            timestr = "  "
        msg.strip("\n")
        if "\n" in msg:
            if addtime:
                msg = ("\n" + msg).replace("\n", "\n  ")
            else:
                msg = ("\n" + msg).replace("\n", "\n  ").strip("\n")
        if spr["ShowConsole"]:
            self.infobox.append(timestr + msg)
            self.infobox.ensureCursorVisible()
        logger.info(msg)

    def infoHead(self):
        today = strftime("%Y-%m-%d", localtime())
        if today != logger.date:
            logger.new_handler(today)
        now_time = strftime("%Y-%m-%d", localtime())
        if spr["ShowConsole"]:
            self.infobox.append(now_time)

    def infoEnd(self):
        _str = "------------------------------"
        if spr["ShowConsole"]:
            self.infobox.append(_str)
            self.infobox.ensureCursorVisible()
        logger.info(_str)

    def infoClear(self):
        if spr["ShowConsole"]:
            self.infobox.clear()
