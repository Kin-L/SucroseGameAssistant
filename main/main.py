from main.tools.logger import logger
from main.tools.prepare import Prepare


# 检测SGA窗口
sga_prepare = Prepare()
if sga_prepare.find_hwnd((1, "Qt5152QWindowIcon", "砂糖代理")):
    logger.info("SGA早已启动")
    sga_prepare.foreground()
    exit(0)
else:
    # 准备SGA启动环境
    del sga_prepare
    logger.info("================SGA开始启动================")
    import keyboard
    from time import sleep
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from sys import argv
    from .ui.main import MainWindows
    # 唤醒屏幕
    keyboard.press("numlock")
    keyboard.release("numlock")
    sleep(0.01)
    keyboard.press("numlock")
    keyboard.release("numlock")
# SGA窗口初始化
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
application = QApplication(argv)
sga_ui = MainWindows()
application.exec_()

if __name__ == "__main__":
    pass
