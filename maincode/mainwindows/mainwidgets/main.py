from ..mainwindow.main import SGAQMainWindow
from ..mainwidgets.loadwidget import LoadWidget
from ..mainwidgets.mainwidget import MainWidget
from time import localtime, strftime
from maincode.tools.main import logger
from sys import argv
from maincode.tools.constant import spr


class SGAMainWidgets:
    def __init__(self):
        self.SGAQMW = SGAQMainWindow()
        if spr["LoadUI"]:
            self.loading = LoadWidget(self.SGAQMW)
            self.SGAQMW.show()
            # 窗口显现
            from maincode.tools.main import GetWindow
            self.window = GetWindow("砂糖代理")
            if "back" not in argv:
                self.window.foreground()

            self.mainwidget = MainWidget()
            self.SGAQMW.setCentralWidget(self.mainwidget)

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
            self.mainwidget.infobox.append(timestr + msg)
            self.mainwidget.infobox.ensureCursorVisible()
        logger.info(msg)

    def infoHead(self):
        today = strftime("%Y-%m-%d", localtime())
        if today != logger.date:
            logger.new_handler(today)
        now_time = strftime("%Y-%m-%d", localtime())
        if spr["ShowConsole"]:
            self.mainwidget.infobox.append(now_time)

    def infoEnd(self):
        _str = "------------------------------"
        if spr["ShowConsole"]:
            self.mainwidget.infobox.append(_str)
            self.mainwidget.infobox.ensureCursorVisible()
        logger.info(_str)

    def infoClear(self):
        if spr["ShowConsole"]:
            self.mainwidget.infobox.clear()
