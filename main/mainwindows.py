from main.ui.overall.window import OverallWindow
from main.ui.module.window import ModuleWindow
from sys import exit as sysexit
from traceback import format_exc
from main.mainenvironment import sme
from main.tools.logger import logger
from main.ui.mainwindow.window import MainWindow
from time import strftime, localtime
from datetime import datetime


class MainWindows:
    def __init__(self):
        self.state = {}
        # 载入主窗口
        try:
            self.main = MainWindow()
        except Exception as err:
            sme.send_messagebox("主窗口加载异常(1/6):\n%s\n" % err)
            logger.critical("主窗口加载异常(1/6):\n%s\n" % format_exc())
            sysexit(1)
        # 载入全局设置窗口
        try:
            self.overall = OverallWindow(self.main.stack_setting)
        except Exception as err:
            sme.send_messagebox("全局设置窗口加载失败(2/6):\n%s\n" % err)
            logger.critical("全局设置窗口加载失败(2/6):\n%s\n" % format_exc())
            sysexit(1)
        # 载入模组设置窗口
        try:
            self.module = ModuleWindow(self.main.stack_setting)
            self.main.stack_setting.setCurrentIndex(1)
            self.overall.label_version.setText(sme.version)
        except Exception as err:
            sme.send_messagebox("模组设置窗口加载失败(3/6):\n%s\n" % err)
            logger.critical("模组设置窗口加载失败(3/6):\n%s\n" % format_exc())
            sysexit(1)

    def sendbox(self, msg="", mode=0):
        if mode == 0:  # 时间前缀的信息持续追加
            txt = (strftime("%H:%M:%S ", localtime()) + msg).replace("\n", "\n    ")
            self.main.box_info.append(txt)
            self.main.box_info.ensureCursorVisible()
        elif mode == 1:  # 时间前缀的信息头部追加
            date = datetime.now().strftime("%Y-%m-%d")
            if date != logger.date:
                logger.new_handler(date)
            now_time = strftime("%Y-%m-%d", localtime())
            self.main.box_info.append(now_time)
        elif mode == 2:  # 直接追加信息
            self.main.box_info.append(msg)
            self.main.box_info.ensureCursorVisible()
        elif mode == 3:  # 信息段落结尾
            self.main.box_info.append("------------------------------")
            self.main.box_info.ensureCursorVisible()
        else:
            print("信息输出,无效模式")

    # 时间前缀的信息持续追加
    def indicate(self, msg=""):
        txt = (strftime("%H:%M:%S ", localtime()) + msg).replace("\n", "\n    ")
        self.main.box_info.append(txt)
        self.main.box_info.ensureCursorVisible()
        logger.info(msg)

    @staticmethod
    def logger_version():
        logger.info(f"用户窗口构建完成，SGA版本:{sme.version}")


smw = MainWindows()
