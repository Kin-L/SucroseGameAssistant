from main.ui.overall.main import OverallWindow
from main.ui.module.main.module import ModuleWindow
from sys import exit as sysexit
from traceback import format_exc
from main.tools.environment import env
from main.tools.logger import logger
from .control import PicButton, Button, Picture, Stack
from .ui_part import Support, InfoBox, OverallButton, MainWidget
from time import strftime, localtime
from datetime import datetime
from os.path import exists, splitext
from os import listdir, makedirs
from random import randint
from shutil import copyfile


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
        self.state = {}
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
        elif mode == 2:  # 信息段落结尾
            self.main.box_info.append("------------------------------")
            self.main.box_info.ensureCursorVisible()
        elif mode == 3:  # 直接追加信息
            self.main.box_info.append(msg)
            self.main.box_info.ensureCursorVisible()
        else:
            print("信息输出,无效模式")

    # 时间前缀的信息持续追加
    def indicate(self, msg=""):
        txt = (strftime("%H:%M:%S ", localtime()) + msg).replace("\n", "\n    ")
        self.main.box_info.append(txt)
        self.main.box_info.ensureCursorVisible()
        logger.info(msg)

    def read_main_config(self):
        _config = {
            "work_path": "",
            "lock": True,
            "config": "",
            "update": False,
            "timer": {},
            "current": {"模块": 0}
        }
        from json import load, dump
        if exists(r"personal/main_config.json"):
            # noinspection PyBroadException
            try:
                with open(r"personal/main_config.json", 'r', encoding='utf-8') as c:
                    config = load(c)
            except Exception:
                # noinspection PyBroadException
                try:
                    with open(r"personal/main_config_bak.json", 'r', encoding='utf-8') as c:
                        config = load(c)
                    with open(r"personal/main_config.json", 'w', encoding='utf-8') as c:
                        dump(config, c, ensure_ascii=False, indent=1)
                    self.indicate("主配置文件损坏,从备份中恢复")
                except Exception:
                    config = {}
                    self.indicate("备份配置文件损坏,主配置文件重置")
        _config.update(config)
        # 获取设置及分类
        if not exists("personal/config"):
            makedirs("personal/config")
        _listdir = listdir("personal/config")
        if not _listdir:
            newname = "默认配置" + str(randint(999, 10000))
            copyfile(r"assets\main_window\default_config.json",
                     r"personal\config\00%s.json" % newname)
            _listdir = listdir("personal/config")
        for file in listdir("personal/config"):
            name, suffix = splitext(file)
            if suffix == ".json":
                prefix = name[:2]
                name = name[2:]
                if prefix == "00":
                    env.serial += [name]
                elif prefix in env.prefix[1:]:
                    env.single += [name]
                else:
                    continue
                env.plan = prefix


main_windows = MainWindows()
