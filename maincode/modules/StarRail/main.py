from ..main import ModuleClass
from .widget import StarRailPage
from .task.main import taskstart
from maincode.modules.template import SubConfigTemplate


class StarRailConfig(SubConfigTemplate):
    ModuleKey: int = 5
    path: str = "D:\March7thAssistant\March7th Launcher.exe"
    timeout: int = 0  # 超时关闭时间，单位分钟




class StarRailClass(ModuleClass):
    def __init__(self):
        self.ModuleKey = 5
        self.ModuleNameCH = "崩坏：星穹铁道"
        self.ModuleNameEN = "star_rail"
        self.IconPath = 'resources/StarRail/StarRail-icon.png' 
        self.Config = StarRailConfig
        self.Widget = StarRailPage()
        self.Task = taskstart
        super().__init__()
