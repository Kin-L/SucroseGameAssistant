import maincode.tools.system.window
from maincode.tools.core.logger import logger
from maincode.tools.system.notification import SendMessageBox, GetTracebackInfo, CheckAdmin
from maincode.tools.system.window import GetWindow
from PyQt5.QtCore import Qt
from time import sleep
from maincode.tools.core.constant import spr
from maincode.sgamain import SGAMain
from PyQt5.QtWidgets import QApplication
import keyboard
import sys


def SGALoad(showconsole: bool = True):
    try:
        spr["ShowConsole"] = showconsole

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
            load_ui = not (showconsole and ("current" in sys.argv or "hideui" in sys.argv))
            spr["LoadUI"] = load_ui

            if load_ui:
                QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
                QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
                QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
                application = QApplication(sys.argv)

                sqm = SGAMain()
                if "current" in sys.argv:
                    sqm.TaskStart(sqm.SMW, "current")
                application.exec_()
            else:
                sqm = SGAMain()
                logger.info("SGA启动完成, SGA运行中...")
                if "current" in sys.argv:
                    sqm.TaskStart(sqm.SMW, "current")

            logger.info("==================SGA关闭=================\n\n")
    except Exception as e:
        _str = GetTracebackInfo(e) + "SGA加载失败"
        logger.critical(_str)
        SendMessageBox(_str)


if __name__ == "__main__":
    pass
