import os.path
import json
from main.ui.overall.window import OverallWindow
from main.ui.module.window import ModuleWindow
from sys import exit as sysexit
from traceback import format_exc
from main.tools.environment import env
from main.tools.logger import logger
from main.ui.mainwindow.window import MainWindow
from time import strftime, localtime
from datetime import datetime
from os.path import exists, splitext
from os import listdir, makedirs
from random import randint
from shutil import copyfile


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

    def read_main_config(self):
        _config = {
            "current_work_path": "",
            "timer": {},
            "update": False,
            "lock": True,
            "config": "",
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
                    config = _config
                    self.indicate("备份配置文件损坏,主配置文件重置")
        else:
            config = _config
        # noinspection PyBroadException
        try:
            env.current_work_path = config["current_work_path"]
            env.timer = config["timer"]
            env.update = config["update"]
            env.lock = config["lock"]
            env.config = config["config"]
            env.current = config["current"]
            if not env.current["模块"] in list(range(len(env.name))):
                env.current["模块"] = 0
        except Exception:
            self.indicate("配置文件损坏,主配置文件重置")
            env.current_work_path = _config["current_work_path"]
            env.timer = _config["timer"]
            env.update = _config["update"]
            env.lock = _config["lock"]
            env.config = _config["config"]
            env.current = _config["current"]
        # 获取设置及分类
        if not exists("personal/config"):
            makedirs("personal/config")
        _listdir = listdir("personal/config")
        if not _listdir:
            newname = "默认配置" + str(randint(999, 10000))
            copyfile(r"assets\main_window\default_config.json",
                     r"personal\config\%s.json" % newname)
            _listdir = listdir("personal/config")
        _dir = os.path.join(env.workdir, "personal/config")
        for file in listdir(_dir):
            name, suffix = splitext(file)
            if suffix == ".json":
                _path = os.path.join(_dir, file)
                # noinspection PyBroadException
                try:
                    with open(_path, 'r', encoding='utf-8') as c:
                        _config = json.load(c)
                    if _config["模块"] < len(env.name):
                        pass
                    else:
                        continue
                except Exception:
                    continue
                env.config_name += [name]
                env.config_type += [_config["模块"]]


main_windows = MainWindows()
