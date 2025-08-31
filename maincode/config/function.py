from maincode.config.maingroup import sg
from maincode.config.mainconfig import TimerConfigClass
from maincode.tools.main import GetTracebackInfo
from maincode.mainwindows.timer.function import ApplyTimer
from maincode.tools.main import logger
from maincode.tools.constant import spr


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
            if self.mw.sksetting.currentIndex():
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
