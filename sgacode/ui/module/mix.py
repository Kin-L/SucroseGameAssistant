from sgacode.ui.module.moduleclass import ModuleClass
from sgacode.configclass import ScheMa, ConfigTool
from sgacode.ui.control import (Combobox, SetStackPage,
                                ModuleStackPage, Widget, Line,
                                Picture)
from typing import List
from sgacode.tools.main import env


class MixClass(ModuleClass):
    def __init__(self):
        self.ModuleNum = ModuleClass.Count
        self.ModuleKey = 0
        self.ModuleNameCH = "连续任务"
        self.ModuleNameEN = "mix"
        self.IconPath = 'resources/main/SGA/default.png'

        schema = {
                  'ConfigKey': {'type': str, 'default': ""},
                  'ModuleKey': {'type': int, 'default': self.ModuleKey},
                  'ConfigName': {'type': str, 'default': "默认配置"},
                  'ConfigKeyList': {'type': List[int], 'default': [0] * 8},
                  '静音': {'type': bool, 'default': False},
                  '关闭软件': {'type': bool, 'default': True},
                  '完成后': {'type': int, 'default': 0},
                  'SGA关闭': {'type': bool, 'default': False},
                  }
        self.schema = ScheMa(schema)
        super().__init__()
        self.Config = ConfigTool(self.schema)
        self.PageClass = MixPage


class MixPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.wdlist = MixList()
        self.srlist.setWidget(self.wdlist)
        self.page01 = MixPage01Set()
        self.sksetting.addWidget(self.page01)
        Line(self, (215, 5, 3, 530), False)
        pic = 'resources/main/SGA/title.png'
        self.picbt = Picture(self, (175, 5, 35, 35), pic)

    def LoadWindow(self, config: dict):
        super().LoadWindow(config)
        ckl = config['ConfigKeyList']
        sccl: list = list(zip(*env.value["SubConfigs"]))[0]
        _list = []
        for k in ckl:
            if k in sccl:
                _list += [sccl.index(k) + 1]
            else:
                _list += [0]
        self.wdlist.task01.setCurrentIndex(_list[0])
        self.wdlist.task02.setCurrentIndex(_list[1])
        self.wdlist.task03.setCurrentIndex(_list[2])
        self.wdlist.task04.setCurrentIndex(_list[3])
        self.wdlist.task05.setCurrentIndex(_list[4])
        self.wdlist.task06.setCurrentIndex(_list[5])
        self.wdlist.task07.setCurrentIndex(_list[6])
        self.wdlist.task08.setCurrentIndex(_list[7])


class MixList(Widget):
    def __init__(self):
        super().__init__()
        self.task01 = Combobox(self, (0, 0, 210, 35))
        self.task02 = Combobox(self, (0, 45, 210, 35))
        self.task03 = Combobox(self, (0, 90, 210, 35))
        self.task04 = Combobox(self, (0, 135, 210, 35))
        self.task05 = Combobox(self, (0, 180, 210, 35))
        self.task06 = Combobox(self, (0, 225, 210, 35))
        self.task07 = Combobox(self, (0, 270, 210, 35))
        self.task08 = Combobox(self, (0, 315, 210, 35))

        namelist: list = ["<未选择>"] + list(list(zip(*env.value["SubConfigs"]))[2])
        self.task01.addItems(namelist)
        self.task02.addItems(namelist)
        self.task03.addItems(namelist)
        self.task04.addItems(namelist)
        self.task05.addItems(namelist)
        self.task06.addItems(namelist)
        self.task07.addItems(namelist)
        self.task08.addItems(namelist)


class MixPage01Set(SetStackPage):
    def __init__(self):
        super().__init__("运行方式：")
