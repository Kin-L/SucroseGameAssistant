from traceback import format_exc
from PyQt5.QtCore import QThread
from time import sleep
from main.tools.logger import logger
from main.ui.mainwindow.connect import save_env_data
from main.ui.overall.timer.connect import check_timer
from main.mainenvironment import sme
from main.ui.module.connect import read_config_dir
from datetime import datetime
import sys


class SGAThread(QThread):
    def __init__(self, _mode="cycle"):
        super().__init__()
        self.mode = _mode

    def run(self):
        if self.mode == "cycle":
            # noinspection PyBroadException
            try:
                sleep(10)
                while 1:
                    if _text := check_timer():
                        sme.last_runtime = datetime.now().strftime("%Y-%m-%d %H:%M")
                        save_env_data()
                        sme.now_config = read_config_dir(_text)
                        sme.now_config["name"] = _text
                        print("定时任务开始")
                        break
                    sleep(10)
                    save_env_data()
                    sleep(10)
            except Exception as err:
                sme.send_messagebox("时间循环线程异常:\n%s\n" % err)
                logger.error("时间循环线程异常:\n%s\n" % format_exc())
                sys.exit(1)
        elif self.mode == "autoupdate":
            pass
        else:
            logger.debug(f"SGA线程异常参数启动(mode)：{self.mode}")
