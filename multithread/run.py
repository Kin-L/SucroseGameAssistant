# -*- coding: utf-8 -*-
from ui.main.main_top import *
from ui.element.control import *
import traceback
from PyQt5.QtCore import QThread, pyqtSignal
from task.main import TaskRun


class Kill(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super().__init__()
        self.ui = ui

    def run(self):
        # noinspection PyBroadException
        try:
            import keyboard
            keyboard.wait("ctrl+/")
            self.ui.state["wait_time"] = 5
            foreground(self.ui.state["hwnd"])
            self.ui.sga_run.terminate()
            pixmap = QPixmap(r"assets/main_window/ui/ico/2.png")
            self.indicate("手动终止", 3)
            env.OCR.disable()
            self.ui.button_pause.hide()
            self.ui.button_start.show()
            self.ui.label_status.setPixmap(pixmap)
        except Exception:
            logger.error("手动终止线程异常:\n%s\n" % traceback.format_exc())
            sys.exit(1)

    def indicate(self, msg: str, mode=2, his=True, log=True):
        self.send.emit(msg, mode, his, log)


class SGARun(QThread, TaskRun):
    send = pyqtSignal(str, int, bool, bool)
    pause = pyqtSignal(int)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super(SGARun, self).__init__()
        self.ui = ui

    def run(self):
        _k = False
        if not env.OCR.check():
            self.indicate("OCR缺失,开始下载安装")
            if not self.install_ocr():
                _k = True
        if not _k:
            # noinspection PyBroadException
            try:
                if self.task_start(self.ui.task):
                    _k = True
            except Exception:
                _k = True
                logger.error("执行流程异常:\n%s" % traceback.format_exc())
        # noinspection PyBroadException
        try:
            self.kill(_k)
        except Exception:
            logger.error("结束流程异常:\n%s\n" % traceback.format_exc())

    def indicate(self, msg: str, mode=2, his=True, log=True):
        self.send.emit(msg, mode, his, log)

    def install_ocr(self):
        # noinspection PyBroadException
        try:
            from urllib.request import urlretrieve
            import requests
            import json
            temp_path = os.path.join(env.workdir, "cache")
            temp_name = os.path.basename(env.OCR.exe_name + ".zip")
            load_path = os.path.join(temp_path, temp_name)
            load = "https://gitee.com/api/v5/repos/huixinghen/SucroseGameAssistant/releases?page=1&per_page=20"
            response = requests.get(load, timeout=10)
            if response.status_code == 200:
                urlretrieve(env.OCR.load_url, load_path)
                self.indicate("下载完成,开始安装")
            else:
                self.indicate(f"连接错误(code {response.status_code})")
                raise ValueError(f"连接错误(code {response.status_code})")
        except Exception:
            self.indicate("下载异常")
            logger.error("下载异常:\n%s\n" % traceback.format_exc())
            return False
        # noinspection PyBroadException
        try:
            from shutil import unpack_archive
            unpack_archive(load_path, temp_path)
        except Exception:
            self.indicate("解压异常")
            logger.error("解压异常:\n%s\n" % traceback.format_exc())
            return False
        # noinspection PyBroadException
        try:
            from shutil import copytree
            extract_folder = os.path.splitext(load_path)[0]
            cover_folder = os.path.join(env.workdir, "3rd_package", env.OCR.exe_name)
            copytree(extract_folder, cover_folder, dirs_exist_ok=True)
        except Exception:
            self.indicate("替换异常")
            logger.error("替换异常:\n%s\n" % traceback.format_exc())
            return False
        # noinspection PyBroadException
        try:
            from shutil import rmtree
            os.remove(load_path)
            rmtree(extract_folder)
        except Exception:
            self.indicate("删除临时文件异常")
            logger.error("删除临时文件异常:\n%s\n" % traceback.format_exc())
            return False
        # 弹窗重启
        self.indicate(f"安装成功:{cover_folder}")
        return True

    def kill(self, mode):
        self.ui.state["wait_time"] = 5
        foreground(self.ui.state["hwnd"])
        if mode:
            _str0 = "异常"
            pixmap = QPixmap(r"assets/main_window/ui/ico/3.png")
        else:
            _str0 = "完成"
            pixmap = QPixmap(r"assets/main_window/ui/ico/1.png")
        self.ui.label_status.setPixmap(pixmap)
        # 通知
        if self.ui.task["name"]:
            _text = f"{_str0}执行:定时计划"
            notify(_text, "任务名:" + self.ui.task["name"])
            self.indicate(_text + self.ui.task["name"])
        else:
            _text = f"{_str0}执行:实时计划"
            notify(f"{_str0}执行:实时计划", " ")
            self.indicate(_text)
        if self.ui.task["完成后"] == 1:
            self.indicate("任务完成,20s后熄屏")
            self.indicate("         可按组合键“ctrl+/”取消", 4, False)
        elif self.ui.task["完成后"] == 2:
            self.indicate("  任务完成,60s后睡眠")
            self.indicate("         可按组合键“ctrl+/”取消", 4, False)
        now_mute = get_mute()
        if (now_mute != self.ui.task["current_mute"]) and (now_mute == self.ui.task["静音"]):
            wait(1000)
            move(50, 50)
            wait(200)
            change_mute()
        # 结束
        if self.ui.task["完成后"] == 1:
            wait(20000)
            self.ui.kill.terminate()
            self.ui.button_pause.hide()
            self.ui.button_start.show()
            if self.ui.task["SGA关闭"]:
                self.indicate("SGA关闭 电脑熄屏", 3)
                cmd_run("start "" /d \"assets/main_window/bat_scr\" screen_off.vbs")
                sys.exit(0)
            else:
                self.indicate("SGA等待 电脑熄屏", 3)
                screen_off()
        elif self.ui.task["完成后"] == 2:
            wait(60000)
            self.ui.kill.terminate()
            self.ui.button_pause.hide()
            self.ui.button_start.show()
            if self.ui.task["SGA关闭"]:
                self.indicate("SGA关闭 电脑睡眠", 3)
                cmd_run("start "" /d \"assets/main_window/bat_scr\" sleep.vbs")
                sys.exit(0)
            else:
                self.indicate("SGA等待 电脑睡眠", 3)
                self.ui.state["wait_time"] = 5
                self.ui.cycle.start()
                cmd_run("start "" /d \"assets/main_window/bat_scr\" sleep.vbs")
        else:
            self.ui.kill.terminate()
            if self.ui.task["SGA关闭"]:
                self.indicate("SGA关闭 电脑无操作", 3)
                sys.exit(0)
            else:
                self.ui.button_pause.hide()
                self.ui.button_start.show()
                self.ui.state["wait_time"] = 5
                self.indicate("SGA等待 电脑无操作", 3)
                self.ui.cycle.start()
