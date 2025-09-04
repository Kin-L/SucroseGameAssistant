from maincode.config.configctrl import scc
from maincode.tools.system.notification import GetTracebackInfo
from maincode.tools.core.logger import logger
from maincode.mainwindows.mainwindow import SGAQMainWindow
from maincode.mainfunc.check import timercheck, updatecheck
from maincode.mainfunc.taskctrl import TaskStart, TaskStop, ManualStop, NewThread, handle_finished_action
from maincode.mainfunc.config import currentsave, subconfigsave, SaveConfig, ManualSaveConfig
from maincode.mainwindows.overall.main import SGAOverall
from maincode.mainwindows.module.main import SGAModule
from typing import Optional
import keyboard
from PyQt5.QtWidgets import QApplication
from maincode.tools.system.other import CmdRun


class SGAMain(SGAQMainWindow):
    def __init__(self):
        super().__init__()
        self._bind_class_methods()
        self.SG.Load()
        self.OCR.clear()
        logger.info(self.SG.info.GetEnvironmentInfoStr())
        self.overall: Optional[SGAOverall] = None
        self.module: Optional[SGAModule] = None
        self.LoadUI = False

    def load_ui(self):
        self.LoadUI = True
        self._init_loading_ui()
        self.overall = SGAOverall(self)
        self.module = SGAModule(self)
        self._connect_signals_loadui()
        self.loading.hide()
        self.loading.lower()
        self.infoAdd("加载完成", False)
        self.infoEnd()

    def _bind_class_methods(self):
        self.__class__.currentsave = currentsave
        self.__class__.subconfigsave = subconfigsave
        self.__class__.SaveConfig = SaveConfig
        self.__class__.ManualSaveConfig = ManualSaveConfig
        self.__class__.TaskStart = TaskStart
        self.__class__.TaskStop = TaskStop
        self.__class__.handle_finished_action = handle_finished_action
        self.__class__.NewThread = NewThread
        self.__class__.ManualStop = ManualStop
        self.__class__.timercheck = timercheck
        self.__class__.updatecheck = updatecheck

    def _connect_signals_loadui(self):
        self.mainwidget.sksetting.addWidget(self.overall.widget)
        self.overall.widget.btsupport.clicked.connect(self.mainwidget.support.show)
        self.mainwidget.sksetting.addWidget(self.module.widget)
        self.mainwidget.sksetting.setCurrentIndex(1)
        self.timer.timeout.connect(self.timercheck)
        self.timer.start(15000)
        self.module.widget.btstart.clicked.connect(self.btstart_mode)
        self.module.widget.btpause.clicked.connect(self.ManualStop)
        self.overall.widget.btcheckupdate.clicked.connect(self.updatecheck)
        self.mainwidget.btconfigsave.clicked.connect(self.ManualSaveConfig)
        self.quicksave.activated.connect(self.ManualSaveConfig)
        self.overall.widget.btrestart.clicked.connect(self.restart)

    def btstart_mode(self):
        if scc.mc.StartMode == "Down":
            self.TaskStart("current")
        else:
            self.TaskStart("subconfig", {"num": self.module.widget.ecbconfig.currentIndex()})

    def hideui_connect(self):
        for i in self.SG.loadstate.items():
            if i[1]:
                logger.info(i[0])
        self.timer.timeout.connect(self.timercheck)
        self.timer.start(15000)
        logger.info("SGA启动，当前为无UI模式")
        logger.infoEnd()

    def closeEvent(self, event):
        try:
            if hasattr(self, 'threadpool') and hasattr(self.threadpool, 'quit'):
                self.threadpool.quit()
                self.threadpool.wait()
                self.threadpool.deleteLater()
        except Exception as e:
            logger.error(f"线程池退出异常: {GetTracebackInfo(e)}")

        try:
            if hasattr(self, 'OCR'):
                self.OCR.disable()
            keyboard.unhook_all()
            if self.LoadUI:
                self.SG.mc.ModulesEnable = [
                    self.module.widget.boxmodule.itemText(i)
                    for i in range(self.module.widget.boxmodule.count())
                ]
                self.SaveConfig()
            super().closeEvent(event)
        except Exception as e:
            logger.error(f"SGA退出前清理资源异常: {GetTracebackInfo(e)}")
        finally:
            event.accept()

    @staticmethod
    def restart():
        # 重启程序
        CmdRun("start \"\" /d \"personal/script\" start-SGA.vbs")
        app = QApplication.instance()
        if app:
            app.quit()
