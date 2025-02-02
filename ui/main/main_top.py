from .main_up import MainUp
from tools.environment import *
from sys import exit as sysexit
from os import startfile
from tools.software import *
from PyQt5.QtGui import QPixmap
from traceback import format_exc
from webbrowser import open as weopen


class MainTop(MainUp):
    def __init__(self):
        super().__init__()
        self.cycle = None
        self.kill = None
        self.sga_run = None
        self.update = None

    def thread_load(self):
        from multithread.cycle import Cycle
        from multithread.run import Kill, SGARun
        from multithread.update import Update
        self.cycle = Cycle(self)
        self.kill = Kill(self)
        self.sga_run = SGARun(self)
        self.update = Update(self)

    def function_connect(self):
        # 主面板操作
        self.button_set_home.toggled.connect(self.change_interface)
        self.button_sponsor.clicked.connect(self.window_support.show)
        self.button_statement.clicked.connect(self.show_statement)
        self.button_instructions.clicked.connect(lambda: cmd_run("start "" Instructions.docx"))
        self.button_history.clicked.connect(lambda: cmd_run("start /d \"personal\" history.txt"))
        # 全局设置操作
        self.overall.timer.apply.clicked.connect(self.apply_timer)
        self.overall.button_check.clicked.connect(self.check_update)
        self.overall.button_update.clicked.connect(self.load_update)
        self.overall.timer.delete.clicked.connect(self.timer_delete)

        self.overall.button_update_history.clicked.connect(lambda: startfile(env.workdir + "/update_history.txt"))
        self.overall.button_logger.clicked.connect(lambda: startfile(env.workdir + "/personal/logs"))
        self.overall.button_github.clicked.connect(lambda: weopen("https://github.com/Kin-L/SucroseGameAssistant"))
        self.overall.button_gitee.clicked.connect(lambda: weopen("https://gitee.com/huixinghen/SucroseGameAssistant"))
        self.overall.button_bilibili.clicked.connect(lambda: weopen("https://space.bilibili.com/406315493"))
        # 配置操作
        self.button_config_delete.clicked.connect(self.delete_plan)
        self.box_config_change.currentIndexChanged.connect(self.config_change)
        self.box_config_change.editingFinished.connect(self.config_rename)
        self.button_config_lock.clicked.connect(lambda: self.set_config_lock(False))
        self.button_config_unlock.clicked.connect(lambda: self.set_config_lock(True))

        self.button_config_save.clicked.connect(self.save_config)
        self.button_start.clicked.connect(self.start)
        self.button_pause.clicked.connect(self.pause)
        # 切换面板
        self.box_module_change.currentIndexChanged.connect(self.change_module)
        # 信息输出
        self.kill.send.connect(self.indicate)
        self.sga_run.send.connect(self.indicate)
        self.cycle.send.connect(self.indicate)
        self.update.send.connect(self.indicate)

    def check_update(self, mode=0):
        self.overall.button_check.setEnabled(False)
        self.indicate("检查更新中...")
        self.update.mode = mode
        self.update.start()

    def load_update(self):
        self.overall.button_update.setEnabled(False)
        self.update.mode = 1
        self.update.start()

    def start(self, _task=None):
        # noinspection PyBroadException
        try:
            self.cycle.terminate()
            self.save_main_data()
            self.indicate("", 0)
            if _task:
                self.task = _task
            else:
                self.task = self.get_config_run()
            self.task["name"] = ""
            self.task["current_mute"] = get_mute()
            if self.task["静音"] and not self.task["current_mute"]:
                change_mute()
            self.box_info.clear()
            self.indicate("", 1)
            self.indicate("开始执行:实时计划")
            pixmap = QPixmap(r"assets\main_window\ui\ico\0.png")
            self.label_status.setPixmap(pixmap)
            self.button_pause.show()
            self.button_start.hide()

            self.kill.start()
            self.sga_run.start()
        except Exception:
            logger.error("手动开始异常:\n%s\n" % format_exc())
            sysexit(1)

    def pause(self):
        # noinspection PyBroadException
        try:
            self.state["wait_time"] = 5
            foreground(self.state["hwnd"])
            # noinspection PyBroadException
            try:
                self.sga_run.trigger.kill()
            except Exception:
                pass
            self.sga_run.terminate()
            pixmap = QPixmap(r"assets/main_window/ui/ico/2.png")
            self.indicate("手动终止", 3)
            env.OCR.disable()
            self.button_pause.hide()
            self.button_start.show()
            self.label_status.setPixmap(pixmap)
            self.kill.terminate()
            self.cycle.start()
        except Exception:
            logger.error("手动终止线程异常:\n%s\n" % format_exc())
            sysexit(1)
