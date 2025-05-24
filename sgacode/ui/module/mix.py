from sgacode.ui.module.moduleclass import ModuleClass
from sgacode.tools.main import ConfigTool
from sgacode.tools.myclass import ScheMa


class MixClass(ModuleClass):
    def __init__(self):
        self.ModuleNum = ModuleClass.Count
        self.ModuleKey = 0
        self.ModuleNameCH = "连续任务"
        self.ModuleNameEN = "mix"
        self.IconPath = 'resources/main/SGA/icon.png'

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
