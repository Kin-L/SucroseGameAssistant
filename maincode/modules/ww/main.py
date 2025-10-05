from ..main import ModuleClass
from .widget import wwPage
from .task.main import taskstart
from maincode.modules.template import SubConfigTemplate


class wwConfig(SubConfigTemplate):
    ModuleKey: int = 7
    path: str = "D:\ok-ww\ok-ww.exe"
    timeout: int = 0  # 超时关闭时间，单位分钟




class wwClass(ModuleClass):
    def __init__(self):
        self.ModuleKey = 7
        self.ModuleNameCH = "鸣潮"
        self.ModuleNameEN = "Wuthering Waves"
        self.IconPath = 'resources/ww/ww-icon.png'
        self.Config = wwConfig
        self.Widget = wwPage()
        self.Task = taskstart
        self.LoadModule = True
        super().__init__()
