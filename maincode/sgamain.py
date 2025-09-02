from maincode.tools.system.notification import GetTracebackInfo
from maincode.tools.core.logger import logger
from maincode.mainwindows.mainwindow import SGAQMainWindow
from maincode.tools.core.constant import spr
from maincode.mainfunc.check import timercheck, updatecheck
from maincode.mainfunc.taskctrl import TaskStart, TaskStop, ManualStop, NewThread
from maincode.mainfunc.config import currentsave, subconfigsave, SaveConfig, ManualSaveConfig
from maincode.mainwindows.overall.main import SGAOverall
from maincode.mainwindows.module.main import SGAModule
import keyboard


class SGAMain(SGAQMainWindow):
    def __init__(self):
        super().__init__()
        self._bind_class_methods()
        self.SG.Load()
        self.OCR.clear()
        logger.info(self.SG.info.GetEnvironmentInfoStr())
        if spr["LoadUI"]:
            self.overall = SGAOverall(self)
            self.module = SGAModule(self)
            self._connect_signals()
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
        self.__class__.NewThread = NewThread
        self.__class__.ManualStop = ManualStop
        self.__class__.timercheck = timercheck
        self.__class__.updatecheck = updatecheck

    def _connect_signals(self):
        self.mainwidget.sksetting.addWidget(self.overall.widget)
        self.overall.widget.btsupport.clicked.connect(self.mainwidget.support.show)
        self.mainwidget.sksetting.addWidget(self.module.widget)
        self.mainwidget.sksetting.setCurrentIndex(1)
        self.timer.timeout.connect(self.timercheck)
        self.timer.start(15000)
        self.module.widget.btstart.clicked.connect(lambda: self.TaskStart("current"))
        self.module.widget.btpause.clicked.connect(self.ManualStop)
        self.overall.widget.btcheckupdate.clicked.connect(self.updatecheck)
        self.mainwidget.btconfigsave.clicked.connect(self.ManualSaveConfig)
        self.quicksave.activated.connect(self.ManualSaveConfig)

    def closeEvent(self, event):
        try:
            if hasattr(self, 'worker') and hasattr(self.worker, 'quit'):
                self.worker.quit()
                self.worker.wait()
                self.worker.deleteLater()
        except Exception as e:
            logger.error(f"Worker线程退出异常: {GetTracebackInfo(e)}")

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
            if spr["LoadUI"]:
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
