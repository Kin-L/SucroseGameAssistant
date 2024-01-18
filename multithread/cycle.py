# -*- coding: utf-8 -*-
from ui.main.main_top import *
from ui.element.control import *
import traceback
from PyQt5.QtCore import QThread, pyqtSignal
from task.main import TaskRun
from pyautogui import press as papress
import time


class Cycle(QThread, TaskRun):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super(Cycle, self).__init__()
        self.ui = ui

    def run(self):
        # noinspection PyBroadException
        try:
            for i in range(self.ui.state["wait_time"]):
                time.sleep(6)
                self.ui.save_main_data()
            while 1:
                text = self.ui.check_timer()
                if text:
                    self.time_to_run(text)
                    break
                time.sleep(10)
                self.ui.save_main_data()
                time.sleep(10)
        except Exception:
            logger.error("时间循环线程异常:\n%s\n" % traceback.format_exc())
            sys.exit(1)

    def indicate(self, msg: str, mode=2, his=True, log=True):
        self.send.emit(msg, mode, his, log)

    def time_to_run(self, mode: str = ""):
        papress("numlock")
        wait(100)
        papress("numlock")
        self.indicate("", 0)
        self.ui.task = self.ui.get_config_run(mode)
        self.ui.task["name"] = mode
        self.ui.task["current_mute"] = get_mute()
        if self.ui.task["静音"] and not self.ui.task["current_mute"]:
            change_mute()
        self.indicate("", 1)
        _name = self.ui.task["name"]
        self.indicate(f"开始执行:定时计划 {_name}")
        notify("开始定时任务", f"任务名:{_name}")

        pixmap = QPixmap(r"assets/main_window/ui/ico/0.png")
        self.ui.label_status.setPixmap(pixmap)
        self.ui.button_pause.show()
        self.ui.button_start.hide()

        self.ui.kill.start()
        self.ui.sga_run.start()
