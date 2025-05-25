from sgacode.ui.module.moduleclass import ModuleClass
from sgacode.tools.main import ConfigTool
from sgacode.configclass import ScheMa
from sgacode.ui.control import (Combobox, Stack, SetStackPage,
                                ModuleStackPage, Widget, Line,
                                Picture)


class MixClass(ModuleClass):
    def __init__(self):
        self.ModuleNum = ModuleClass.Count
        self.ModuleKey = 0
        self.ModuleNameCH = "连续任务"
        self.ModuleNameEN = "mix"
        self.IconPath = 'resources/main/SGA/default.png'

        schema = {'ModuleKey': {'type': int, 'default': self.ModuleKey},
                  'ConfigName': {'type': str, 'default': None},
                  '静音': {'type': bool, 'default': False},
                  '关闭软件': {'type': bool, 'default': True},
                  '完成后': {'type': int, 'default': 0},
                  'SGA关闭': {'type': bool, 'default': False},
                  }
        self.schema = ScheMa(schema)
        super().__init__()
        self.Config = ConfigTool(self.schema)

    def WidgetInit(self, stack: Stack):
        super().WidgetInit(stack)
        self.Widget = MixPage()
        stack.addWidget(self.Widget)


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


class MixPage01Set(SetStackPage):
    def __init__(self):
        super().__init__("运行方式：")
