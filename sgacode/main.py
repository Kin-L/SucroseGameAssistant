from time import sleep, strftime, localtime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QThread
from sgacode.ui.main import SGAQMainWindow
from sgacode.tools.main import (logger, env, GetHwnd,
                                CheckAdmin, SendMessageBox,
                                GetTracebackInfo)
from sys import argv
import keyboard


class SGAMAIN:
    def __init__(self, useui: bool):
        super().__init__()
        self.thread = QThread()  # 线程初始化
        if useui:
            self.SQMW = SGAQMainWindow(self.thread)  # 显示窗口初始化界面
            self.SMW = self.SQMW.LoadMainWindows()  # 加载主窗口
        from sgacode.configclass import SGAMainConfig
        from sgacode.ui.module.moduleclass import SGAModuleGroup
        from sgacode.thread import SGAMainThread
        # 配置信息加载
        self.SMC = SGAMainConfig()  # 加载主配置信息
        self.SMG = SGAModuleGroup(self.SMC)  # 加载子配置信息
        if useui:
            self.SMW.LoadMainSet(self.SMC)  # 加载主设置
            self.SMW.LoadSubSet(self.SMC, self.SMG)  # 加载子设置
        # 主线程加载
        self.SMT = SGAMainThread(self.SMC, self.SMG)
        self.SMT.moveToThread(self.thread)
        if useui:
            self.InfoBox = self.SMW.infobox
            self.LoadMainConnect()  # 加载状态链接
        self.thread.start()

    def EnterMainWindows(self):
        self.SQMW.loading.hide()
        self.SQMW.loading.lower()

    def LoadMainConnect(self):
        self.SMT.info.connect(self.info)
        self.SMT.infoHead.connect(self.infoHead)
        self.SMT.infoEnd.connect(self.infoEnd)

    def info(self, msg: str = "", addtime=True):
        addstr = ""
        if addtime:
            addstr += strftime("%H:%M:%S ", localtime())
        msg.strip("\n")
        if "\n" in msg:
            addstr += "\n" + ("\n" + msg).replace("\n", "  ")
        else:
            addstr += msg
        self.InfoBox.append(addstr)
        self.InfoBox.ensureCursorVisible()

    def infoHead(self):
        today = strftime("%Y-%m-%d", localtime())
        if today != logger.date:
            logger.new_handler(today)
        now_time = strftime("%Y-%m-%d", localtime())
        self.InfoBox.append(now_time)

    def infoEnd(self):
        self.InfoBox.append("------------------------------")
        self.InfoBox.ensureCursorVisible()


def SGA(useui: bool = True):
    try:
        CheckAdmin()
        env.hwnd = GetHwnd(True, "Qt5152QWindowIcon", "砂糖代理")
        if env.hwnd:
            env.foreground()
            # exit(0)
        else:
            print("")
            logger.info("================SGA开始启动================")
            # 唤醒屏幕
            keyboard.send("numlock")
            sleep(0.01)
            keyboard.send("numlock")
            env.logger_environment_info()
            # SGA窗口初始化
            QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
            application = QApplication(argv)
            sgamain = SGAMAIN(useui)
            if useui:
                sgamain.EnterMainWindows()
            application.exec_()
            logger.info("==================SGA关闭=================\n\n")
    except Exception as e:
        _str = GetTracebackInfo(e) + "\nSGA加载失败"
        logger.critical(_str)
        SendMessageBox(_str)
        # exit(1)


if __name__ == "__main__":
    pass
