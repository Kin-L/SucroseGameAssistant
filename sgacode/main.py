from sgacode.tools.main import (logger, env, gethwnd,
                                checkadmin, sendmessagebox,
                                gettracebackinfo)
from sgacode.configclass import SGAMainConfig
from sgacode.ui.main import SGAQMainWindow
from sys import argv
import keyboard
from time import sleep
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from sgacode.ui.module.moduleclass import SGAModuleGroup


class SGAMAIN:
    def __init__(self):
        super().__init__()
        # 配置信息加载
        self.SMC = SGAMainConfig()  # 加载主配置信息
        self.SMG = SGAModuleGroup(self.SMC)  # 加载子配置信息
        # 主线程加载
        self.LoadMainThread()
        # 加载窗口
        self.SQMW = SGAQMainWindow()  # 显示窗口初始化界面
        self.SMW = self.SQMW.LoadMainWindows(self.SMG)  # 加载窗口
        self.LoadMainConnect()  # 加载状态链接
        self.SQMW.loading.hide()
        self.SQMW.loading.lower()

    def LoadMainThread(self):
        pass

    def LoadMainConnect(self):
        pass


try:
    checkadmin()
    env.hwnd = gethwnd(True, "Qt5152QWindowIcon", "砂糖代理")
    if env.hwnd:
        env.foreground()
        exit(0)
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
        sgamain = SGAMAIN()
except Exception as e:
    _str = gettracebackinfo(e) + "\nSGA加载失败"
    logger.critical(_str)
    sendmessagebox(_str)
    exit(1)
application.exec_()
logger.info("==================SGA关闭=================\n\n")

if __name__ == "__main__":
    pass
