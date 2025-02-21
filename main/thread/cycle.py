from traceback import format_exc
from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep
from main.mainwindows import main_windows as mw
from main.ui.mainwindow.connect import save_env_data
from main.ui.overall.timer.connect import check_timer
from main.tools.environment import env, logger
from main.tools.system import notify, get_mute
from main.ui.module.connect import read_config_dir
import sys


class Cycle(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super(Cycle, self).__init__()
        self.ui = ui

    def run(self):
        # noinspection PyBroadException
        try:
            for i in range(env.wait_time):
                sleep(10)
            save_env_data()
            while 1:
                if text := check_timer():
                    self.time_to_run(text)
                    break
                sleep(10)
                save_env_data()
                sleep(10)
        except Exception:
            logger.error("时间循环线程异常:\n%s\n" % format_exc())
            sys.exit(1)

    def time_to_run(self, mode: str = ""):
        import keyboard
        keyboard.press("numlock")
        keyboard.release("numlock")
        sleep(0.01)
        keyboard.press("numlock")
        keyboard.release("numlock")
        notify("SGA 定时任务", f"10秒后开始 任务名:{mode}")
        sleep(10)
        save_env_data()
        mw.box_info.clear()
        env.now_config = read_config_dir(mode)
        env.now_config["name"] = mode
        env.current_mute = get_mute()
        if self.ui.task["静音"] and not env.current_mute:
            keyboard.press('volumemute')
        mw.sendbox(mode=1)
        _name = self.ui.task["name"]
        mw.indicate(f"开始执行:定时计划 {_name}")
        notify("开始定时任务", f"任务名:{_name}")

        self.ui.button_pause.show()
        self.ui.button_start.hide()

        self.ui.kill.start()
        self.ui.sga_run.start()
