from ..main import ModuleClass
from .widget import GenshinPage
from .task.main import taskstart
from maincode.modules.template import SubConfigTemplate


class GenshinConfig(SubConfigTemplate):
    ModuleKey: int = 4
    bgipath: str = "D:\BetterGI\BetterGI.exe"
    timeout: int = 0  # 超时关闭时间，单位分钟




class GenshinClass(ModuleClass):
    ModuleNameCH = "原神"
    def __init__(self):
        self.ModuleKey = 4
        self.ModuleNameEN = "Genshin"
        self.IconPath = 'resources/genshin/genshin-icon.png'
        self.Config = GenshinConfig
        self.Widget = GenshinPage()
        self.Task = taskstart
        self.LoadModule = True
        super().__init__()
