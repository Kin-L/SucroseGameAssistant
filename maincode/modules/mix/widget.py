from maincode.tools.controls import (Combobox, SetStackPage,
                                     ModuleStackPage, Widget, Line,
                                     Picture, TaskPanel, Label)
from typing import Optional
from maincode.main.subconfig import sc


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

        # self.picbt =

    def SetWidget(self, config: dict):
        seql = [sc.FindItem(k)[-1]+1 if k else 0 for k in config['ConfigKeyList']]
        self.wdlist.task01.setCurrentIndex(seql[0])
        self.wdlist.task02.setCurrentIndex(seql[1])
        self.wdlist.task03.setCurrentIndex(seql[2])
        self.wdlist.task04.setCurrentIndex(seql[3])
        self.wdlist.task05.setCurrentIndex(seql[4])
        self.wdlist.task06.setCurrentIndex(seql[5])
        self.wdlist.task07.setCurrentIndex(seql[6])
        self.wdlist.task08.setCurrentIndex(seql[7])
        self.page01.taskpanel.ckkillsga.setChecked(config["SGAClose"])
        self.page01.taskpanel.ckmute.setChecked(config["Mute"])
        self.page01.taskpanel.ckkillprog.setChecked(True)
        self.page01.taskpanel.cbafter.setCurrentIndex(config["Finished"])

    def CollectConfig(self) -> dict:
        _dict = dict()
        _list = [
            self.wdlist.task01.currentIndex()-1,
            self.wdlist.task02.currentIndex()-1,
            self.wdlist.task03.currentIndex()-1,
            self.wdlist.task04.currentIndex()-1,
            self.wdlist.task05.currentIndex()-1,
            self.wdlist.task06.currentIndex()-1,
            self.wdlist.task07.currentIndex()-1,
            self.wdlist.task08.currentIndex()-1, ]
        _dict['ConfigKeyList'] = [sc.filelist[i][0] if i > -1 else "" for i in _list]
        _dict["Mute"] = self.page01.taskpanel.ckmute.isChecked()
        _dict["SoftClose"] = True
        _dict["Finished"] = self.page01.taskpanel.cbafter.currentIndex()
        _dict["SGAClose"] = self.page01.taskpanel.ckkillsga.isChecked()
        return _dict


class MixList(Widget):
    def __init__(self):
        super().__init__()
        self.lbsubtask = Label(self, (5, 0, 120, 27), "子任务选择：")
        self.task01 = Combobox(self, (0, 40, 210, 35))
        self.task02 = Combobox(self, (0, 85, 210, 35))
        self.task03 = Combobox(self, (0, 130, 210, 35))
        self.task04 = Combobox(self, (0, 175, 210, 35))
        self.task05 = Combobox(self, (0, 220, 210, 35))
        self.task06 = Combobox(self, (0, 265, 210, 35))
        self.task07 = Combobox(self, (0, 310, 210, 35))
        self.task08 = Combobox(self, (0, 355, 210, 35))

        namelist: list = ["<未选择>"] + [name for ck, name, mk in sc.filelist]
        self.task01.addItems(namelist)
        self.task02.addItems(namelist)
        self.task03.addItems(namelist)
        self.task04.addItems(namelist)
        self.task05.addItems(namelist)
        self.task06.addItems(namelist)
        self.task07.addItems(namelist)
        self.task08.addItems(namelist)


class MixPage00Set(SetStackPage):
    def __init__(self):
        super().__init__("运行方式：")
        self.taskpanel = TaskPanel(self, 55)
        self.taskpanel.ckkillprog.setDisabled(True)
