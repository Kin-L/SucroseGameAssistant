from sys import argv
from main.tools.logger import logger
from main.mainenvironment import sme
from main.mainwindows import smw
from traceback import format_exc
from sys import exit as sysexit
from main.ui.connect import load_main_config, function_connect


def main_connect():
    # 加载主配置
    try:
        load_main_config()
    except Exception as err:
        sme.send_messagebox("主配置加载失败(4/6):\n%s\n" % err)
        logger.critical("主配置加载失败(4/6):\n%s\n" % format_exc())
        sysexit(1)
    # 功能链接
    try:
        # 功能键链接
        function_connect()
    except Exception as err:
        sme.send_messagebox("状态链接失败(5/6):\n%s\n" % err)
        logger.critical("状态链接失败(5/6):\n%s\n" % format_exc())
        sysexit(1)
    try:
        # 窗口显现
        smw.main.label_shelter.hide()
        smw.main.widget.show()
        sme.find_hwnd((1, "Qt5152QWindowIcon", "砂糖代理"))
        if len(argv) <= 1:
            sme.foreground()
        elif argv[1] != "True":
            sme.foreground()
    except Exception as err:
        sme.send_messagebox("用户界面显现失败(6/6):\n%s\n" % err)
        logger.critical("用户界面显现失败(6/6):\n%s\n" % format_exc())
        sysexit(1)
