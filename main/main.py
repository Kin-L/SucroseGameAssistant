from main.tools.logger import Logger
from main.tools.prepare import Prepare
logger = Logger().get_logger()
logger.info("============SGA开始启动============")
logger.info("日志启动")

# 检测SGA窗口
sga_prepare = Prepare(logger)
_hwnd = sga_prepare.find_hwnd((1, "Qt5152QWindowIcon", "砂糖代理"))
if _hwnd:
    logger.info("SGA早已启动")
    sga_prepare.foreground()
    exit(0)
else:
    del _hwnd, sga_prepare
    logger.info("SGA开始启动")
    import keyboard
    from time import sleep
    from main.tools.environment import Environment
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from sys import argv
    # 唤醒屏幕
    keyboard.press("numlock")
    sleep(0.1)
    keyboard.press("numlock")
env = Environment(logger)

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
application = QApplication(argv)
application.exec_()
