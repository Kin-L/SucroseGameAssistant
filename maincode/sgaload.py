from maincode.tools.main import (CheckAdmin, GetWindow, logger,
                                 GetTracebackInfo, SendMessageBox)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from time import sleep
from maincode.tools.constant import spr
import keyboard
import sys


def excepthook(exc_type, exc_value, exc_tb):
    logger.critical("全局异常", exc_info=(exc_type, exc_value, exc_tb))
    # SendMessageBox(f"崩溃: {exc_value}")


sys.excepthook = excepthook


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
            from maincode.thread.updatecheck import SGAMain8
            if showconsole and ("current" in sys.argv or "hideui" in sys.argv):
                spr["LoadUI"] = False
            else:
                spr["LoadUI"] = True
            sqmw = SGAMain8()
            if not spr["LoadUI"]:
                logger.info("SGA启动完成, SGA运行中...")
                if "current" in sys.argv:
                    sqmw.TaskStart("current")
            application.exec_()
            logger.info("==================SGA关闭=================\n\n")
    except Exception as e:
        _str = GetTracebackInfo(e) + "SGA加载失败"
        logger.critical(_str)
        SendMessageBox(_str)


if __name__ == "__main__":
    pass
