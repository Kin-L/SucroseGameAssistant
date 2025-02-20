from sys import argv
from main.tools.logger import logger
from main.tools.environment import env
from main.mainwindows import main_windows as mw
from traceback import format_exc
from sys import exit as sysexit
from main.ui.connect import load_main_config, function_connect


def main_connect():
    # 加载主配置
    try:
        mw.read_main_config()
        load_main_config()
    except Exception as err:
        env.send_messagebox("主配置加载失败(4/7):\n%s\n" % err)
        logger.critical("主配置加载失败(4/7):\n%s\n" % format_exc())
        sysexit(1)
    # try:
    #     sga_ui.thread_load()
    # except Exception as err:
    #     env.send_messagebox("线程加载失败(5/7):\n%s\n" % err)
    #     logger.critical("线程加载失败(5/7):\n%s\n" % format_exc())
    #     sysexit(1)
    # # 功能链接
    try:
        # 功能键链接
        function_connect()
    except Exception as err:
        env.send_messagebox("状态链接失败(6/7):\n%s\n" % err)
        logger.critical("状态链接失败(6/7):\n%s\n" % format_exc())
        sysexit(1)
    # try:

    #     if sga_ui.config["update"]:
    #         sga_ui.check_update(2)
    #     sga_ui.cycle.start()
    # except Exception as err:
    #     env.send_messagebox("线程开启失败(7/7):\n%s\n" % err)
    #     logger.critical("线程开启失败(7/7):\n%s\n" % format_exc())
    #     sysexit(1)
    try:
        # 窗口显现
        mw.main.label_shelter.hide()
        mw.main.widget.show()
        env.find_hwnd((1, "Qt5152QWindowIcon", "砂糖代理"))
        if len(argv) > 1:
            if argv[1] == "True":
                pass
            else:
                env.foreground()
        else:
            env.foreground()
    except Exception as err:
        env.send_messagebox("窗口显现失败(8/8):\n%s\n" % err)
        logger.critical("窗口显现失败(8/8):\n%s\n" % format_exc())
        sysexit(1)
