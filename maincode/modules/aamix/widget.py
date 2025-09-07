from maincode.tools.sgaqt.texts import Label, Picture, Line
from maincode.tools.sgaqt.buttons import Combobox
from maincode.tools.sgaqt.widgets import Widget, SetStackPage, ModuleStackPage, TaskPanel
from typing import Optional
from maincode.config.subconfig import subconfig


class MixPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.wdlist: Optional[MixList] = None
        self.page01: Optional[MixPage00Set] = None
        pic = 'resources/main/SGA/title.png'
        self.picbt = Picture(self, (175, 5, 35, 35), pic)

    def LoadWidget(self):
        self.wdlist = MixList()
        self.srlist.setWidget(self.wdlist)
        self.page01 = MixPage00Set()
        self.sksetting.addWidget(self.page01)
        Line(self, (215, 5, 3, 530), False)

    def SetWidget(self, config: dict):
        seql = [subconfig.FindItem(k)[-1] + 1 if k else 0 for k in config['ConfigKeyList']]
        for i in range(len(self.wdlist.tasks)):
            self.wdlist.tasks[i].setCurrentIndex(seql[i])
        self.page01.taskpanel.ckkillsga.setChecked(config["SGAClose"])
        self.page01.taskpanel.ckmute.setChecked(config["Mute"])
        self.page01.taskpanel.ckkillprog.setChecked(True)
        self.page01.taskpanel.cbafter.setCurrentIndex(config["Finished"])

    def CollectConfig(self) -> dict:
        _dict = dict()
        _list = [
            i.currentIndex()-1 for i in self.wdlist.tasks
        ]
        _dict['ConfigKeyList'] = [subconfig.filelist[i][0] if i > -1 else "" for i in _list]
        _dict["Mute"] = self.page01.taskpanel.ckmute.isChecked()
        _dict["SoftClose"] = True
        _dict["Finished"] = self.page01.taskpanel.cbafter.currentIndex()
        _dict["SGAClose"] = self.page01.taskpanel.ckkillsga.isChecked()
        return _dict


class MixList(Widget):
    def __init__(self):
        super().__init__()
        self.lbsubtask = Label(self, (5, 0, 120, 27), "子任务选择：")
        self.tasks = []
        namelist: list = ["<未选择>"] + [name for ck, name, mk in subconfig.filelist]
        for i in range(8):
            _cb = Combobox(self, (0, 45 * i + 35, 210, 35))
            _cb.addItems(namelist)
            self.tasks.append(_cb)


class MixPage00Set(SetStackPage):
    def __init__(self):
        super().__init__("运行方式：")
        self.taskpanel = TaskPanel(self, 55)
        self.taskpanel.ckkillprog.setDisabled(True)
