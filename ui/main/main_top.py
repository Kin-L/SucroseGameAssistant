from .main_up import MainUp
from tools.environment import *
import sys
from tools.software import *
from PyQt5.QtGui import QPixmap
import traceback


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
        self.button_instructions.clicked.connect(lambda: cmd_run("start "" SGA使用说明.docx"))
        self.button_history.clicked.connect(lambda: cmd_run("start /d \"personal\" history.txt"))
        self.panel_restart.restart.clicked.connect(self.restart)
        # 全局设置操作
        self.overall.timer.apply.clicked.connect(self.apply_timer)
        self.overall.button_update.clicked.connect(self.check_update)
        self.overall.timer.delete.clicked.connect(self.timer_delete)
        # 配置操作
        self.button_config_delete.clicked.connect(self.delete_plan)
        self.box_config_change.currentTextChanged.connect(self.config_change)
        self.button_config_lock.clicked.connect(lambda: self.set_config_lock(False))
        self.button_config_unlock.clicked.connect(lambda: self.set_config_lock(True))
        self.button_config_save.clicked.connect(self.save_config)
        self.button_start.clicked.connect(self.start)
        self.button_pause.clicked.connect(self.pause)
        # 切换面板
        self.mix.button_mix.clicked.connect(lambda: self.change_module(0))
        self.kleins.button_klein.clicked.connect(lambda: self.change_module(1))
        self.genshin.button_genshin.clicked.connect(lambda: self.change_module(2))
        self.maa.button_maa.clicked.connect(lambda: self.change_module(3))
        self.m7a.button_m7a.clicked.connect(lambda: self.change_module(4))
        # 信息输出
        self.kill.send.connect(self.indicate)
        self.sga_run.send.connect(self.indicate)
        self.cycle.send.connect(self.indicate)
        self.update.send.connect(self.indicate)

    def check_update(self):
        self.overall.button_update.setEnabled(False)
        self.indicate("检查更新中...")
        self.update.start()

    def restart(self):
        self.panel_restart.widget.hide()
        cmd_run("start "" /d \"personal/bat\" restart.vbs")
        sys.exit(0)

    def start(self):
        # noinspection PyBroadException
        try:
            self.cycle.terminate()
            self.indicate("", 0)
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
            logger.error("手动开始异常:\n%s\n" % traceback.format_exc())
            sys.exit(1)

    def pause(self):
        # noinspection PyBroadException
        try:
            self.state["wait_time"] = 5
            SetForegroundWindow(self.state["hwnd"])
            self.sga_run.terminate()
            pixmap = QPixmap(r"../assets/main_window/ui/ico/2.png")
            self.indicate("手动终止", 3)
            if env.OCR:
                env.OCR.disable()
            self.button_pause.hide()
            self.button_start.show()
            self.label_status.setPixmap(pixmap)
        except Exception:
            logger.error("手动终止线程异常:\n%s\n" % traceback.format_exc())
            sys.exit(1)
