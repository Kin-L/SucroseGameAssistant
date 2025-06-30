from .module.main import SGAMain5
from maincode.main.maingroup import sg
from maincode.main.mainconfig import TimerConfigClass
from maincode.tools.main import GetTracebackInfo, logger
from .timer.function import ApplyTimer


class SGAMain6(SGAMain5):
    def __init__(self, userui):
        super().__init__(userui)

    def SaveConfig(self):
        sg.mainconfig.TimerConfig = TimerConfigClass(**self.CollectConfig())
        num = self.module.boxmodule.currentIndex()
        mk = sg.modules.GetInfos()[num][2]
        _dict = {'ModuleKey': mk, 'ConfigKey': "", 'ConfigName': "默认配置"}
        _subconfig = sg.modules.GetWidgets()[num].CollectConfig()
        _subconfig.update(_dict)
        otherconfig = _subconfig.pop("OtherConfig", {})
        sg.mainconfig.OtherConfig.update(otherconfig)
        sg.mainconfig.CurrentConfig = _subconfig

        smc = sg.mainconfig.model_dump()
        if smc != sg.currentmainconfig:
            sg.SaveMain()
            sg.SaveBackUp()
            sg.currentmainconfig = smc

    def ManualSaveConfig(self):
        self.infoHead()

        # self.SaveConfig()
        if self.mainwidget.sksetting.currentIndex():
            _dict = {'ConfigKey': sg.mainconfig.ConfigKey,
                     'ConfigName': self.module.ecbconfig.text()}
            _save = dict(sg.mainconfig.CurrentConfig)
            _save.update(_dict)
            sg.subconfig.Save(_save)
            num = sg.subconfig.FindItem(_save['ConfigKey'])[-1]
            sg.subconfig.filelist[num][2] = _save['ModuleKey']
            self.infoAdd("保存成功", False)
        else:
            try:
                sg.mainconfig.TimerConfig = TimerConfigClass(**self.CollectConfig())
                if ApplyTimer():
                    self.infoAdd("应用SGA定时自启/唤醒", False)
                else:
                    self.infoAdd("取消SGA自启/唤醒行为", False)
            except Exception as e:
                _str = GetTracebackInfo(e) + "操作异常：更改SGA定时自启/唤醒"
                logger.error(_str)
                self.infoAdd("操作异常：更改SGA定时自启/唤醒", False)
        self.infoEnd()

    def closeEvent(self, event):
        self.SaveConfig()
        try:
            if self.thread.isRunning():
                self.thread.quit()
                self.thread.wait()
        except Exception as e:
            print(e)
        super().closeEvent(event)
