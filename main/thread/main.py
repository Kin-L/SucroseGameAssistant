from traceback import format_exc
from PyQt5.QtCore import QThread
from time import sleep
from main.tools.logger import logger
from main.ui.mainwindow.connect import save_env_data
from main.ui.overall.timer.connect import check_timer
from main.mainenvironment import sme
from main.mainwindows import smw
from main.ui.module.connect import read_config_dir
from datetime import datetime
from .update import check_update, update_procedure
import keyboard
import sys


class SGAThread(QThread):
    def __init__(self, _mode="cycle"):
        super().__init__()
        self.mode = _mode

    def run(self):
        if self.mode == "cycle":
            smw.main.label_shelter.hide()
        elif self.mode == "autoupdate":
            if check_update():
                update_procedure()
            smw.main.label_shelter.hide()
        elif self.mode == "contactupdate":
            smw.main.label_shelter.show()
            update_procedure()
            smw.main.label_shelter.hide()
        elif self.mode == "contacttask":
            sme.last_runtime = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_env_data()
            sme.now_config = smw.module.collect_module_config()
            sme.now_config["name"] = "current"
            print("触发任务开始")
            from .task import contact_task
            contact_task()
        else:
            sme.send_messagebox(f"SGA线程异常参数启动(mode)：{self.mode}")
            logger.debug(f"SGA线程异常参数启动(mode)：{self.mode}")
            sys.exit(1)
        # noinspection PyBroadException
        try:
            sleep(10)
            while 1:
                if _text := check_timer():
                    sme.last_runtime = datetime.now().strftime("%Y-%m-%d %H:%M")
                    save_env_data()
                    sme.now_config = read_config_dir(_text)
                    sme.now_config["name"] = _text
                    print("定时任务开始")  # appointtask
                    from .task import appoint_task
                    appoint_task()
                sleep(10)
                save_env_data()
                sleep(10)
        except Exception as err:
            sme.send_messagebox("时间循环线程异常:\n%s\n" % err)
            logger.error("时间循环线程异常:\n%s\n" % format_exc())
            sys.exit(1)


class HotKeyStop:
    def __init__(self):
        self.enable = self.hotkeystop_enable
        self.disable = self.hotkeystop_disable
        self.hotkey = False

    def hotkeystop_enable(self):
        keyboard.add_hotkey("ctrl+/", self.thread_stop)
        self.hotkey = True

    def hotkeystop_disable(self):
        if self.hotkey:
            keyboard.remove_hotkey("ctrl+/")
            self.hotkey = False

    def thread_stop(self):
        self.hotkeystop_disable()
        if sme.thread.isRunning():
            sme.thread.terminate()
            smw.indicate("手动终止")
            smw.sendbox(mode=3)
            sme.ocr.disable()
            smw.module.button_pause.hide()
            smw.module.button_start.show()
            from time import sleep
            from datetime import datetime
            _now = datetime.now()
            if sme.last_runtime == _now.strftime("%Y-%m-%d %H:%M"):
                from main.ui.mainwindow.connect import save_env_data
                _num = (60 - int(_now.strftime("%S"))) // 15 + 1
                for i in range(_num):
                    sleep(15)
                    save_env_data()
            sme.thread = SGAThread("cycle")
            sme.thread.start()
        else:
            logger.debug("线程早已关闭")
