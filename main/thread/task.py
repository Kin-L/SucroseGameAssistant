from os import rename, remove, path, makedirs
from main.mainenvironment import sme, logger
from main.mainwindows import smw
from traceback import format_exc
from PyQt5.QtCore import QThread, pyqtSignal
from subprocess import run as cmd_run
from main.tools.system import notify, screen_off, get_mute
from time import sleep
import sys, keyboard


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
            sme.wait_time = 5
            sme.foreground()
            # noinspection PyBroadException
            try:
                self.ui.sga_run.trigger.kill()
            except Exception:
                pass
            self.ui.sga_run.terminate()

            pixmap = QPixmap(r"assets/main_window/ui/ico/2.png")
            smw.indicate("手动终止", 3)
            sme.OCR.disable()
            self.ui.button_pause.hide()
            self.ui.button_start.show()
            self.ui.label_status.setPixmap(pixmap)
            self.ui.cycle_thread.start()
        except Exception:
            logger.error("手动终止线程异常:\n%s\n" % format_exc())
            sys.exit(1)


class SGARun(QThread):
    send = pyqtSignal(str, int, bool, bool)
    pause = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        _k = False
        if not sme.OCR.check():
            smw.indicate("OCR缺失,开始下载安装(下载可能较慢,可选择以下链接或按照使用说明进行手动下载："
                          "https://gitee.com/huixinghen/SucroseGameAssistant/releases "
                          "https://wwp.lanzn.com/b033h9ybi 密码:1siv)")
            if not self.install_ocr():
                _k = True
        if not _k:
            # noinspection PyBroadException
            try:
                if self.task_start(self.ui.task_thread):
                    _k = True
            except Exception:
                sc = screenshot()
                import time
                now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
                new_path = f"personal/errorsc/{now}.png"
                if not path.exists(r"personal/errorsc"):
                    makedirs("personal/errorsc")
                rename(sc, new_path)
                logger.error(f"界面截图导出: {new_path}")
                _k = True
                logger.error("执行流程异常:\n%s" % format_exc())
        # noinspection PyBroadException
        try:
            self.kill(_k)
        except Exception:
            logger.error("结束流程异常:\n%s\n" % format_exc())

    def time_to_run(self, mode: str = ""):
        import keyboard
        keyboard.press("numlock")
        keyboard.release("numlock")
        sleep(0.01)
        keyboard.press("numlock")
        keyboard.release("numlock")
        notify("SGA 定时任务", f"10秒后开始 任务名:{mode}")

        smw.box_info.clear()
        smw.sendbox(mode=1)
        smw.sendbox(f"10秒后开始任务:{mode}")
        sleep(10)
        sme.current_mute = get_mute()
        if sme.now_config["静音"] and not sme.current_mute:
            keyboard.press('volumemute')

        _name = self.ui.task_thread["name"]
        smw.indicate(f"开始执行:定时计划 {_name}")
        notify("开始定时任务", f"任务名:{_name}")

        self.ui.button_pause.show()
        self.ui.button_start.hide()

        self.ui.kill.start()
        self.ui.sga_run.start()

    def install_ocr(self):
        # noinspection PyBroadException
        try:
            from urllib.request import urlretrieve
            import requests
            import json
            if not path.exists(r"cache"):
                _path = sme.workdir + "/cache"
                makedirs(_path)
            temp_path = path.join(sme.workdir, "cache")
            temp_name = path.basename(sme.OCR.exe_name + ".zip")
            load_path = path.join(temp_path, temp_name)
            _load = "https://github.moeyy.xyz/"
            response = requests.get(_load, timeout=10)
            if response.status_code == 200:
                urlretrieve(sme.OCR.load_url, load_path)
                smw.indicate("下载完成,开始安装")
            else:
                smw.indicate(f"连接错误(code {response.status_code})")
                raise ValueError(f"连接错误(code {response.status_code})")
        except Exception:
            smw.indicate("下载异常")
            logger.error("下载异常:\n%s\n" % format_exc())
            return False
        # noinspection PyBroadException
        try:
            from shutil import unpack_archive
            unpack_archive(load_path, temp_path)
        except Exception:
            smw.indicate("解压异常")
            logger.error("解压异常:\n%s\n" % format_exc())
            return False
        # noinspection PyBroadException
        try:
            from shutil import copytree
            extract_folder = path.splitext(load_path)[0]
            cover_folder = path.join(sme.workdir, "3rd_package", sme.OCR.exe_name)
            copytree(extract_folder, cover_folder, dirs_exist_ok=True)
        except Exception:
            smw.indicate("替换异常")
            logger.error("替换异常:\n%s\n" % format_exc())
            return False
        # noinspection PyBroadException
        try:
            from shutil import rmtree
            remove(load_path)
            rmtree(extract_folder)
        except Exception:
            smw.indicate("删除临时文件异常")
            logger.error("删除临时文件异常:\n%s\n" % format_exc())
            return False
        # 弹窗重启
        smw.indicate(f"安装成功:{cover_folder}")
        return True

    def kill(self, mode):
        sme.wait_time = 5
        sme.foreground()
        if mode:
            _str0 = "异常"
            pixmap = QPixmap(r"assets/main_window/ui/ico/3.png")
        else:
            _str0 = "完成"
            pixmap = QPixmap(r"assets/main_window/ui/ico/1.png")
        self.ui.label_status.setPixmap(pixmap)
        # 通知
        if self.ui.task_thread["name"]:
            _text = f"{_str0}执行:定时计划"
            notify(_text, "任务名:" + self.ui.task_thread["name"])
            smw.indicate(_text + self.ui.task_thread["name"])
        else:
            _text = f"{_str0}执行:实时计划"
            notify(f"{_str0}执行:实时计划", " ")
            smw.indicate(_text)
        if self.ui.task_thread["完成后"] == 1:
            smw.indicate("任务完成,20s后熄屏")
            smw.indicate("         可按组合键“ctrl+/”取消", 4, False)
        elif self.ui.task_thread["完成后"] == 2:
            smw.indicate("  任务完成,60s后睡眠")
            smw.indicate("         可按组合键“ctrl+/”取消", 4, False)
        now_mute = get_mute()
        if (now_mute != self.ui.task_thread["current_mute"]) and (now_mute == self.ui.task_thread["静音"]):
            sleep(1.2)
            keyboard.press('volumemute')
        # 结束
        if self.ui.task_thread["完成后"] == 1:
            sleep(20)
            self.ui.kill.terminate()
            self.ui.button_pause.hide()
            self.ui.button_start.show()
            if self.ui.task_thread["SGA关闭"]:
                smw.indicate("SGA关闭 电脑熄屏")
                smw.sendbox(mode=3)
                cmd_run("start "" /d \"assets/main_window/bat_scr\" screen_off.vbs")
                sys.exit(0)
            else:
                smw.indicate("SGA等待 电脑熄屏")
                smw.sendbox(mode=3)
                sme.wait_time = 5
                self.ui.cycle_thread.start()
                screen_off()
        elif self.ui.task_thread["完成后"] == 2:
            sleep(60)
            self.ui.kill.terminate()
            self.ui.button_pause.hide()
            self.ui.button_start.show()
            if self.ui.task_thread["SGA关闭"]:
                smw.indicate("SGA关闭 电脑睡眠")
                smw.sendbox(mode=3)
                cmd_run("start "" /d \"assets/main_window/bat_scr\" sleep.vbs")
                sys.exit(0)
            else:
                smw.indicate("SGA等待 电脑睡眠")
                smw.sendbox(mode=3)
                sme.wait_time = 5
                self.ui.cycle_thread.start()
                cmd_run("start "" /d \"assets/main_window/bat_scr\" sleep.vbs")
        else:
            self.ui.kill.terminate()
            if self.ui.task_thread["SGA关闭"]:
                smw.indicate("SGA关闭 电脑无操作")
                smw.sendbox(mode=3)
                sys.exit(0)
            else:
                self.ui.button_pause.hide()
                self.ui.button_start.show()
                sme.wait_time = 5
                smw.indicate("SGA等待 电脑无操作")
                smw.sendbox(mode=3)
                self.ui.cycle_thread.start()
