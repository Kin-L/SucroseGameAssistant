from main.mainenvironment import sme
from main.mainwindows import smw
from subprocess import run as cmd_run
from main.tools.system import notify, screen_off, get_mute
from time import sleep
import keyboard
import sys


def appoint_task():
    keyboard.press("numlock")
    keyboard.release("numlock")
    sleep(0.01)
    keyboard.press("numlock")
    keyboard.release("numlock")
    _task_name = sme.now_config["name"]
    notify("SGA 定时任务", f"10秒后开始 任务名:{_task_name}")
    smw.box_info.clear()
    smw.sendbox(mode=1)
    smw.sendbox(f"10秒后开始任务:{_task_name}")
    smw.module.button_pause.show()
    smw.module.button_start.hide()
    sme.hotkeystop.enable()
    sleep(10)
    smw.indicate(f"开始执行:定时计划 {_task_name}")
    notify("开始定时任务", f"任务名:{_task_name}")
    sme.current_mute = get_mute()
    if sme.now_config["静音"] and not sme.current_mute:
        keyboard.press('volumemute')
        keyboard.release('volumemute')
    main_task()


def contact_task():
    smw.box_info.clear()
    smw.sendbox(mode=1)
    smw.indicate("开始执行:实时计划")
    smw.module.button_pause.show()
    smw.module.button_start.hide()
    sme.hotkeystop.enable()
    sme.current_mute = get_mute()
    if sme.now_config["静音"] and not sme.current_mute:
        keyboard.press('volumemute')
        keyboard.release('volumemute')
    main_task()


def main_task():
    pass


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
