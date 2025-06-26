from maincode.tools.main import (CheckAdmin, GetWindow, logger, foreground,
                                 GetTracebackInfo, SendMessageBox)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from time import sleep
from sys import argv
import keyboard


def SGALoad(useui: bool = True):
    try:
        if not CheckAdmin():
            return
        window = GetWindow("砂糖代理")
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
            application = QApplication(argv)
            from maincode.thread.updatecheck import SGAMain8
            sqmw = SGAMain8(useui)
            application.exec_()
    except Exception as e:
        _str = GetTracebackInfo(e) + "SGA加载失败"
        logger.critical(_str)
        SendMessageBox(_str)
    logger.info("==================SGA关闭=================\n\n")


if __name__ == "__main__":
    pass
