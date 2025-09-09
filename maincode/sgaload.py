from maincode.tools.core.logger import logger
from maincode.tools.system.notification import SendMessageBox, GetTracebackInfo, CheckAdmin
from maincode.tools.system.window import GetWindow
from PyQt5.QtCore import Qt
from time import sleep
from maincode.sgamain import SGAMain
from PyQt5.QtWidgets import QApplication
import keyboard
import sys


def SGALoad():
    try:
        if not CheckAdmin():
            logger.warning("权限不足，SGA 启动失败")
            return
        window = GetWindow("砂糖代理", True)
        if window is not None:
            window.foreground()
        else:
            print("")
            logger.info("================SGA开始启动================")
            # 唤醒屏幕
            try:
                keyboard.send("numlock")
                sleep(0.01)
                keyboard.send("numlock")
            except Exception as e:
                logger.warning(f"唤醒屏幕失败: {e}")
            # 判断是否加载 UI
            hideui = "-hideui" in sys.argv
            # hideui = True
            QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
            application = QApplication(sys.argv)
            sqm = SGAMain()
            if hideui:
                sqm.hideui_connect()
            else:
                sqm.load_ui()
            if "-current" in sys.argv:
                sqm.TaskStart("current")
            elif "-subconfig" in sys.argv:  # ck为子配置文件识别码，为其文件名的前四位数字
                sqm.TaskStart("subconfig", {"ck": sys.argv[sys.argv.index("-subconfig") + 1]})
            application.exec_()
            logger.info("==================SGA关闭=================\n\n")
    except Exception as e:
        _str = GetTracebackInfo(e) + "SGA加载失败"
        logger.critical(_str)
        SendMessageBox(_str)


if __name__ == "__main__":
    pass
