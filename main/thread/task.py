from main.mainenvironment import sme
from main.mainwindows import smw
from subprocess import run as cmd_run
from main.tools.main import notify, screen_off, get_mute
from time import sleep
import keyboard
import sys


def appoint_task():
    keyboard.send("numlock")
    sleep(0.01)
    keyboard.send("numlock")
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
        keyboard.send('volumemute')
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
        keyboard.send('volumemute')
    main_task()


def kill():
    # noinspection PyBroadException
    try:
        sme.foreground()
        _error = ["异常", "完成"][sme.now_config["error"]]
        if sme.thread.mode == "cycle":
            _text = f"{_error}执行:定时计划 "
            notify(_text, "任务名:" + sme.now_config["name"])
            smw.indicate(_text + sme.now_config["name"])
        elif sme.thread.mode == "contacttask":
            _text = f"{_error}执行:实时计划"
            notify(f"{_error}执行:实时计划", " ")
            smw.indicate(_text)
        if sme.now_config["完成后"] == 1:
            smw.indicate("任务完成,20s后熄屏")
            smw.indicate("         可按组合键“ctrl+/”取消")
        elif sme.now_config["完成后"] == 2:
            smw.indicate("  任务完成,60s后睡眠")
            smw.indicate("         可按组合键“ctrl+/”取消")
        now_mute = get_mute()
        if (now_mute != sme.current_mute) and (now_mute == sme.now_config["静音"]):
            sleep(1.2)
            keyboard.send('volumemute')
        # 结束
        if sme.now_config["完成后"] == 1:
            sleep(20)
            _text = "电脑熄屏"
        elif sme.now_config["完成后"] == 2:
            sleep(60)
            _text = "电脑睡眠"
        else:
            _text = "电脑无操作"
        sme.hotkeystop.disable()
        if sme.now_config["SGA关闭"]:
            smw.indicate(f"SGA关闭 {_text}")
            smw.sendbox(mode=3)
            if sme.now_config["完成后"] == 1:
                cmd_run("start "" /d \"assets/main_window/script\" screen_off.vbs", shell=True)
            elif sme.now_config["完成后"] == 2:
                cmd_run("start "" /d \"assets/main_window/script\" sleep.vbs")
            sys.exit(0)
        else:
            smw.module.button_pause.hide()
            smw.module.button_start.show()
            smw.indicate(f"SGA等待 {_text}")
            smw.sendbox(mode=3)
            if sme.now_config["完成后"] == 1:
                screen_off()
            elif sme.now_config["完成后"] == 2:
                cmd_run("start "" /d \"assets/main_window/script\" sleep.vbs")
    except Exception:
        from traceback import format_exc
        smw.indicate("结束流程异常\n%s\n" % format_exc())
        smw.sendbox(mode=3)


def main_task():
    pass
