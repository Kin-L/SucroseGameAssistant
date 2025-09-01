from maincode.tools.main import (logger,
                                 GetTracebackInfo)
from maincode.mainwindows.mainwindow import SGAQMainWindow
from maincode.tools.constant import spr
from maincode.thread.updatecheck import timercheck, updatecheck

import keyboard
from maincode.thread.taskctrl import TaskStart, TaskStop, ManualStop, NewThread
from maincode.config.function import currentsave, subconfigsave, SaveConfig, ManualSaveConfig
from maincode.mainwindows.overall.main import SGAOverall
from maincode.mainwindows.module.main import SGAModule


class SGAMain(SGAQMainWindow):
    def __init__(self):
        super().__init__()
        self.__class__.currentsave = currentsave
        self.__class__.subconfigsave = subconfigsave
        self.__class__.SaveConfig = SaveConfig
        self.__class__.ManualSaveConfig = ManualSaveConfig
        self.SG.Load()
        self.OCR.clear()
        logger.info(self.SG.info.GetEnvironmentInfoStr())
        if spr["LoadUI"]:
            self.overall = SGAOverall()
            self.mainwidget.sksetting.addWidget(self.overall.widget)
            self.overall.widget.btsupport.clicked.connect(self.mainwidget.support.show)
            self.module = SGAModule(self.overall.widget.timer.widgets.wdtime)
            self.mainwidget.sksetting.addWidget(self.module.widget)
            self.mainwidget.sksetting.setCurrentIndex(1)

        self.__class__.TaskStart = TaskStart
        self.__class__.TaskStop = TaskStop
        self.__class__.NewThread = NewThread
        self.__class__.ManualStop = ManualStop
        self.__class__.timercheck = timercheck
        self.__class__.updatecheck = updatecheck
        if spr["LoadUI"]:
            self.module.widget.btstart.clicked.connect(lambda: self.TaskStart("current"))
            self.module.widget.btpause.clicked.connect(lambda: self.ManualStop)
            self.overall.widget.btcheckupdate.clicked.connect(self.updatecheck)
            self.mainwidget.btconfigsave.clicked.connect(self.ManualSaveConfig)
            self.quicksave.activated.connect(self.ManualSaveConfig)
            self.loading.hide()
            self.loading.lower()
            self.infoAdd("加载完成", False)
            self.infoEnd()
        self.timer.timeout.connect(lambda: timercheck(self))
        self.timer.start(15000)

    def closeEvent(self, event):
        try:
            if hasattr(self, 'worker'):
                self.worker.quit()
                self.worker.wait()
                self.worker.deleteLater()
        except:
            ...
        try:
            if hasattr(self, 'thread'):
                self.threadpool.quit()
                self.threadpool.wait()
                self.threadpool.deleteLater()
        except:
            ...
        try:
            if hasattr(self, 'OCR'):
                self.OCR.disable()
            keyboard.unhook_all()
            # keyboard.remove_all_hotkeys()
            if spr["LoadUI"]:
                self.SG.mainconfig.ModulesEnable = [self.module.widget.boxmodule.itemText(i) for i in
                                               range(self.module.widget.boxmodule.count())]
                self.SaveConfig()
            super().closeEvent(event)
        except Exception as e:
            logger.error(f"SGA退出前清理资源异常: {GetTracebackInfo(e)}")
        finally:
            event.accept()