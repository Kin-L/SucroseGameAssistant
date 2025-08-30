from maincode.tools.main import (CheckAdmin, GetWindow, logger,
                                 GetTracebackInfo, SendMessageBox)
from PyQt5.QtCore import Qt
from time import sleep
from maincode.tools.constant import spr
from maincode.mainwindows.main import SGAMainWindow
from maincode.thread.updatecheck import timercheck, updatecheck
from maincode.thread.taskctrl import TaskStart, TaskStop, ManualStop
from PyQt5.QtWidgets import QShortcut, QApplication
from PyQt5.QtGui import QKeySequence
import keyboard
import sys


class SGAMain:
    def __init__(self):
        self.SMW = SGAMainWindow()
        if spr["LoadUI"]:
            self.SMW.module.btstart.clicked.connect(lambda: TaskStart("current"))
            self.SMW.module.btpause.clicked.connect(ManualStop)
            self.SMW.widget.btcheckupdate.clicked.connect(updatecheck)
            self.SMW.mainwidget.btconfigsave.clicked.connect(self.SMW.ManualSaveConfig)
            self.SMW.quicksave = QShortcut(QKeySequence("Ctrl+S"), self)
            self.SMW.quicksave.activated.connect(self.SMW.ManualSaveConfig)
            # self.quickstop.activated.connect(self.ManualStop)
            self.SMW.loading.hide()
            self.SMW.loading.lower()
            self.SMW.infoAdd("加载完成", False)
            self.SMW.infoEnd()
        self.SMW.timer.timeout.connect(timercheck)
        self.SMW.timer.start(15000)


def SGALoad(showconsole: bool = True):
    try:
        spr["ShowConsole"] = showconsole
        if not CheckAdmin():
            return
        window = GetWindow("砂糖代理", True)
        if window is not None:
            window.foreground()
        else:
            print("")
            logger.info("================SGA开始启动================")
            # 唤醒屏幕
            keyboard.send("numlock")
            sleep(0.01)
            keyboard.send("numlock")
            # SGA窗口初始化
            QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
            application = QApplication(sys.argv)
            if showconsole and ("current" in sys.argv or "hideui" in sys.argv):
                spr["LoadUI"] = False
            else:
                spr["LoadUI"] = True
            sqm = SGAMain()
            if not spr["LoadUI"]:
                logger.info("SGA启动完成, SGA运行中...")
                if "current" in sys.argv:
                    TaskStart(sqm.SMW, "current")
            application.exec_()
            logger.info("==================SGA关闭=================\n\n")
    except Exception as e:
        _str = GetTracebackInfo(e) + "SGA加载失败"
        logger.critical(_str)
        SendMessageBox(_str)


if __name__ == "__main__":
    pass
