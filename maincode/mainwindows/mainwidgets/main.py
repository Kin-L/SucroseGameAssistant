from ..mainwindow.main import SGAMain0
from ..mainwidgets.loadwidget import LoadWidget
from ..mainwidgets.mainwidget import MainWidget
from time import localtime, strftime
from maincode.tools.main import logger
import os
from pathlib import Path as libPath
from sys import argv
from maincode.tools.controls import ConsoleButton


class SGAMain1(SGAMain0):
    def __init__(self, userui):
        super().__init__(userui)
        if self.loadui:
            self.loading = LoadWidget(self)
            self.show()
            # 窗口显现
            from maincode.tools.main import GetWindow
            self.window = GetWindow("砂糖代理")
            if "back" not in argv:
                self.window.foreground()

            self.mainwidget = MainWidget()
            self.setCentralWidget(self.mainwidget)
            if "showconsole" in argv:
                self.mainwidget.btconsole = ConsoleButton(self.mainwidget)
                self.mainwidget.btconsole.setChecked(True)
                self.mainwidget.btconsole.toggled.connect(self.mainwidget.changecs)
            self.mainwidget.btsetting.toggled.connect(self.mainwidget.changeob)
            self.mainwidget.bthistory.clicked.connect(lambda: os.startfile(
                max([f for f in libPath("personal/logs").iterdir() if f.is_file()],
                    key=lambda f: f.stat().st_ctime)))

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
        if self.loadui:
            self.mainwidget.infobox.append(timestr + msg)
            self.mainwidget.infobox.ensureCursorVisible()
        logger.info(msg)

    def infoHead(self):
        today = strftime("%Y-%m-%d", localtime())
        if today != logger.date:
            logger.new_handler(today)
        now_time = strftime("%Y-%m-%d", localtime())
        if self.loadui:
            self.mainwidget.infobox.append(now_time)

    def infoEnd(self):
        _str = "------------------------------"
        if self.loadui:
            self.mainwidget.infobox.append(_str)
            self.mainwidget.infobox.ensureCursorVisible()
        logger.info(_str)

    def infoClear(self):
        if self.loadui:
            self.mainwidget.infobox.clear()
