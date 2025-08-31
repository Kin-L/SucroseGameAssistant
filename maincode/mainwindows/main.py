from maincode.main.maingroup import sg
from maincode.main.mainconfig import TimerConfigClass
from maincode.tools.main import GetTracebackInfo
from .timer.function import ApplyTimer
import keyboard
from maincode.mainwindows.overall.main import SGAOverall
from maincode.mainwindows.module.main import SGAModule
from PyQt5.QtCore import QTimer
from maincode.tools.main import logger
from maincode.tools.ocr.main import OCR
from maincode.tools.constant import spr
from maincode.mainwindows.sgaqmain import SGAQMainWindow
from maincode.mainwindows.mainwidget import MainWidget


class SGAMainWindow(SGAQMainWindow):
    def __init__(self):
        super().__init__()
        if spr["LoadUI"]:
            self.mainwidget = MainWidget()
            self.setCentralWidget(self.mainwidget)
            sg.infoHead.connect(self.mainwidget.infoHead)
            sg.infoAdd.connect(self.mainwidget.infoAdd)
            sg.infoEnd.connect(self.mainwidget.infoEnd)
            self.infoHead = self.mainwidget.infoHead
            self.infoAdd = self.mainwidget.infoAdd
            self.infoEnd = self.mainwidget.infoEnd
        sg.Load()
        OCR.clear()
        logger.info(sg.info.GetEnvironmentInfoStr())
        self.timer = QTimer(self)
        self.sleeptime = 0
        self.timerallow = True
        if spr["LoadUI"]:
            self.overall = SGAOverall()
            self.mainwidget.sksetting.addWidget(self.overall.widget)
            self.overall.widget.btsupport.clicked.connect(self.mainwidget.support.show)
            self.module = SGAModule(self.overall.widget.timer.widgets.wdtime)
            self.mainwidget.sksetting.addWidget(self.module.widget)
            self.mainwidget.sksetting.setCurrentIndex(1)

    def currentsave(self):
        num = self.module.widget.boxmodule.currentIndex()
        mk = sg.modules.GetInfos()[num][2]
        _dict = {'ModuleKey': mk, 'ConfigKey': "", 'ConfigName': "默认配置"}
        _subconfig = sg.modules.GetWidgets()[num].CollectConfig()
        _subconfig.update(_dict)
        otherconfig = _subconfig.pop("OtherConfig", {})
        sg.mainconfig.OtherConfig.update(otherconfig)
        sg.mainconfig.CurrentConfig = _subconfig

    def subconfigsave(self):
        _dict = {'ConfigKey': sg.mainconfig.ConfigKey,
                 'ConfigName': self.module.widget.ecbconfig.text()}
        _save = dict(sg.mainconfig.CurrentConfig)
        _save.update(_dict)
        sg.subconfig.Save(_save)
        num = sg.subconfig.FindItem(_save['ConfigKey'])[-1]
        sg.subconfig.filelist[num][2] = _save['ModuleKey']

    def SaveConfig(self):
        if spr["LoadUI"]:
            self.currentsave()
            sg.mainconfig.TimerConfig = TimerConfigClass(**self.overall.widget.timer.CollectConfig())
            smc = sg.mainconfig.model_dump()
            if smc != sg.currentmainconfig:
                sg.SaveMain()
                sg.SaveBackUp()
                sg.currentmainconfig = smc

    def ManualSaveConfig(self):
        try:
            if spr["LoadUI"] and self.timerallow:
                self.infoHead()
                if self.mainwidget.sksetting.currentIndex():
                    self.currentsave()
                    self.subconfigsave()
                    self.infoAdd("保存成功", False)
                else:
                    try:
                        sg.mainconfig.TimerConfig = TimerConfigClass(**self.overall.widget.timer.CollectConfig())
                        if ApplyTimer():
                            self.infoAdd("应用SGA定时自启/唤醒", False)
                        else:
                            self.infoAdd("取消SGA自启/唤醒行为", False)
                    except Exception as e:
                        _str = GetTracebackInfo(e) + "操作异常：更改SGA定时自启/唤醒"
                        logger.error(_str)
                        self.infoAdd("操作异常：更改SGA定时自启/唤醒", False)
                self.infoEnd()
        except Exception as e:
            _str = GetTracebackInfo(e) + "手动保存流程异常"
            logger.error(_str)
            self.infoAdd(f"手动保存流程异常")

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
                self.thread.quit()
                self.thread.wait()
                self.thread.deleteLater()
        except:
            ...
        try:
            if hasattr(self, 'OCR'):
                self.OCR.disable()
            keyboard.unhook_all()
            # keyboard.remove_all_hotkeys()
            if spr["LoadUI"]:
                sg.mainconfig.ModulesEnable = [self.module.widget.boxmodules.itemText(i) for i in
                                               range(self.module.widget.boxmodules.count())]
                self.SaveConfig()
            super().closeEvent(event)
        except Exception as e:
            logger.error(f"SGA退出前清理资源异常: {GetTracebackInfo(e)}")
        finally:
            event.accept()  # 允许窗口关闭

