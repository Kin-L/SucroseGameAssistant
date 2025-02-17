from main.ui.overall.main import OverallWindow
from main.ui.module.main.module import ModuleWindow
from sys import exit as sysexit
from sys import argv
from traceback import format_exc
from main.tools.environment import env
from main.tools.logger import logger
from .control import PicButton, Button, Picture, Stack
from .ui_part import Support, InfoBox, OverallButton, MainWidget


class MainWindow:
    def __init__(self):
        self.widget = MainWidget()
        self.label_shelter = Picture(self.widget, (0, 0, 910, 580),  # 指示图标
                                     r"assets\main_window\back\set_back.png")
        self.label_shelter.raise_()
        # 全局/模块 设置按钮
        self.button_set_home = OverallButton(self.widget)  # 全局/模块 设置按钮
        self.button_history = PicButton(self.widget, (693, 0, 56, 56),  # 历史信息按钮
                                        r"assets\main_window\button\history.png", (25, 25))
        self.button_sponsor = PicButton(self.widget, (751, 0, 56, 56),  # 赞赏按钮
                                        r"assets\main_window\button\support.png", (25, 25))
        self.window_support = Support()
        self.button_statement = Button(self.widget, (809, 0, 96, 27), "使用须知")
        self.button_instructions = Button(self.widget, (809, 29, 96, 27), "使用说明")
        self.label_status = Picture(self.widget, (485, 430, 150, 150),  # 指示图标
                                    r"assets\main_window\indicate\0.png")
        self.box_info = InfoBox(self.widget)  # 指示信息窗口
        self.stack_setting = Stack(self.widget, (5, 0, 620, 570))


class MainWindows:
    def __init__(self):
        # 载入主窗口
        try:
            self.main = MainWindow()
        except Exception as err:
            env.send_messagebox("主窗口加载异常(1/7):\n%s\n" % err)
            logger.critical("主窗口加载异常(1/7):\n%s\n" % format_exc())
            sysexit(1)
        # 载入全局设置窗口
        try:
            self.overall = OverallWindow(self.main.stack_setting)
        except Exception as err:
            env.send_messagebox("全局设置窗口加载失败(2/7):\n%s\n" % err)
            logger.critical("全局设置窗口加载失败(2/7):\n%s\n" % format_exc())
            sysexit(1)
        # 载入模组设置窗口
        try:
            self.module = ModuleWindow(self.main.stack_setting)
            self.main.stack_setting.setCurrentIndex(1)
        except Exception as err:
            env.send_messagebox("模组设置窗口加载失败(3/7):\n%s\n" % err)
            logger.critical("模组设置窗口加载失败(3/7):\n%s\n" % format_exc())
            sysexit(1)
        # # 加载主配置
        # try:
        #     sga_ui.load_main_config()
        # except Exception as err:
        #     env.send_messagebox("主配置加载失败(4/7):\n%s\n" % err)
        #     logger.critical("主配置加载失败(4/7):\n%s\n" % format_exc())
        #     sysexit(1)
        # try:
        #     sga_ui.thread_load()
        # except Exception as err:
        #     env.send_messagebox("线程加载失败(5/7):\n%s\n" % err)
        #     logger.critical("线程加载失败(5/7):\n%s\n" % format_exc())
        #     sysexit(1)
        # # 功能链接
        # try:
        #     # 功能键链接
        #     sga_ui.function_connect()
        # except Exception as err:
        #     env.send_messagebox("状态链接失败(6/7):\n%s\n" % err)
        #     logger.critical("状态链接失败(6/7):\n%s\n" % format_exc())
        #     sysexit(1)
        # try:
        #     # 全局设置:退出前保存 & 每10秒自动保存
        #     import atexit
        #     atexit.register(sga_ui.exit_save)
        #     if sga_ui.config["update"]:
        #         sga_ui.check_update(2)
        #     sga_ui.cycle.start()
        # except Exception as err:
        #     env.send_messagebox("线程开启失败(7/7):\n%s\n" % err)
        #     logger.critical("线程开启失败(7/7):\n%s\n" % format_exc())
        #     sysexit(1)
        try:
            # 窗口显现
            self.main.label_shelter.hide()
            self.main.widget.show()
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
