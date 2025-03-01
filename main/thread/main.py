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
from sys import exit as sysexit


class SGAThread(QThread):
    def __init__(self, _mode="cycle"):
        super().__init__()
        self.mode = _mode

    def run(self):
        if self.mode == "cycle":
            pass
        elif self.mode == "autoupdate":
            if check_update():
                update_procedure()
        elif self.mode == "contactupdate":
            update_procedure()
        elif self.mode == "contacttask":
            sme.last_runtime = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_env_data()
            sme.now_config = smw.module.collect_module_config()
            sme.now_config["name"] = "current"
            sme.now_config["error"] = False
            print("触发任务开始")
            from .task import contact_task, kill
            # noinspection PyBroadException
            try:
                contact_task()
            except Exception:
                logger.critical("任务执行流程\n%s\n" % format_exc())
                sme.now_config["error"] = True
            kill()
        else:
            sme.send_messagebox(f"SGA线程异常参数启动(mode)：{self.mode}")
            logger.debug(f"SGA线程异常参数启动(mode)：{self.mode}")
            sysexit(1)
        self.mode = "cycle"
        # noinspection PyBroadException
        try:
            sleep(10)
            while 1:
                # 防止同一分钟运行两次
                _now = datetime.now()
                if sme.last_runtime == _now.strftime("%Y-%m-%d %H:%M"):
                    _num = (60 - int(_now.strftime("%S"))) // 15 + 1
                    for i in range(_num):
                        sleep(15)
                        save_env_data()
                # 定时运行
                if _text := check_timer():
                    sme.last_runtime = datetime.now().strftime("%Y-%m-%d %H:%M")
                    save_env_data()
                    sme.now_config = read_config_dir(_text)
                    sme.now_config["name"] = _text
                    sme.now_config["error"] = False
                    print("定时任务开始")  # appointtask
                    from .task import appoint_task, kill
                    # noinspection PyBroadException
                    try:
                        appoint_task()
                    except Exception:
                        logger.critical("任务执行流程\n%s\n" % format_exc())
                        sme.now_config["error"] = True
                    kill()
                sleep(10)
                save_env_data()
                sleep(10)
        except Exception as err:
            sme.send_messagebox("时间循环线程异常:\n%s\n" % err)
            logger.error("时间循环线程异常:\n%s\n" % format_exc())
            sysexit(1)


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
        try:
            self.hotkeystop_disable()
            if sme.thread.isRunning():
                sme.thread.terminate()
                smw.indicate("手动终止")
                smw.sendbox(mode=3)
                sme.ocr.disable()
                smw.module.button_pause.hide()
                smw.module.button_start.show()
                sme.thread = SGAThread("cycle")
                sme.thread.start()
            else:
                logger.debug("线程早已关闭")
        except Exception as err:
            sme.send_messagebox("快捷终止功能异常:\n%s\n" % err)
            logger.critical("快捷终止功能异常:\n%s\n" % format_exc())
            sysexit(1)
