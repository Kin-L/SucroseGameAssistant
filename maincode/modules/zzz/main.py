from ..main import ModuleClass
from .widget import zzzPage
from .task.main import taskstart
from maincode.modules.template import SubConfigTemplate


class zzzConfig(SubConfigTemplate):
    ModuleKey: int = 6
    bgipath: str = "D:\ZenlessZoneZero-OneDragon\OneDragon-Launcher.exe"
    timeout: int = 0  # 超时关闭时间，单位分钟




class zzzClass(ModuleClass):
    def __init__(self):
        self.ModuleKey = 6
        self.ModuleNameCH = "绝区零"
        self.ModuleNameEN = "ZenlessZoneZero"
        self.IconPath = 'resources/zzz/zzz-icon.png'
        self.Config = zzzConfig
        self.Widget = GenshinPage()
        self.Task = taskstart
        super().__init__()
