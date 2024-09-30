from PyQt5.QtWidgets import QApplication
from ui.main.main_top import *
from ui.element.control import *
from ui.element.ui_part import *
from traceback import format_exc
from pyautogui import press as papress
from sys import argv as sysargv
from sys import exit as sysexit
_hwnd = find_hwnd((1, "Qt5152QWindowIcon", "砂糖代理"))
if _hwnd:
    foreground(_hwnd)
    sysexit(1)
# 初始化窗口
papress("numlock")
wait(100)
papress("numlock")
while 1:
    v = get_pid("PaddleOCR-json.exe")
    if v:
        close(v)
    else:
        break
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
application = QApplication(sysargv)
sga_ui = MainTop()
sga_ui.main_window.show()
# 加载主配置
try:
    sga_ui.load_main_config()
except Exception as err:
    message_box("主配置加载失败(4/7):\n%s\n" % err)
    logger.critical("主配置加载失败(4/7):\n%s\n" % format_exc())
    sysexit(1)
try:
    sga_ui.thread_load()
except Exception as err:
    MessageBox(0, "线程加载失败(5/7):\n%s\n" % err, "砂糖代理", MB_OK)
    logger.critical("线程加载失败(5/7):\n%s\n" % format_exc())
    sysexit(1)
# 功能链接
try:
    # 功能键链接
    sga_ui.function_connect()
except Exception as err:
    MessageBox(0, "状态链接失败(6/7):\n%s\n" % err, "砂糖代理", MB_OK)
    logger.critical("状态链接失败(6/7):\n%s\n" % format_exc())
    sysexit(1)
try:
    # 全局设置:退出前保存 & 每10秒自动保存
    import atexit
    atexit.register(sga_ui.exit_save)
    if sga_ui.config["update"]:
        sga_ui.check_update(2)
    sga_ui.cycle.start()
except Exception as err:
    MessageBox(0, "线程开启失败(7/7):\n%s\n" % err, "砂糖代理", MB_OK)
    logger.critical("线程开启失败(7/7):\n%s\n" % format_exc())
    sysexit(1)
logger.info("启动SGA用户界面\n-------------------------------------")
if len(sysargv) > 1:
    if sysargv[1] == "True":
        pass
    else:
        _hwnd = find_hwnd((1, "Qt5152QWindowIcon", "砂糖代理"))
        foreground(_hwnd)
else:
    _hwnd = find_hwnd((1, "Qt5152QWindowIcon", "砂糖代理"))
    foreground(_hwnd)
application.exec_()


if __name__ == "__main__":
    pass
