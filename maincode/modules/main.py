from maincode.modules.template import SubConfigTemplate, ModuleStackPage
from typing import List, Tuple, Callable, Optional

from maincode.tools.core.constant import spr
from maincode.tools.core.logger import logger


def defaulttask(self):
    self.send("任务流程未添加")


class ModuleClass:
    LoadModule: bool = False  # 实例化时，值为真，才加载
    Infos: List[Tuple[str, str, int, str]] = []  # 每个实例的以下四项标识信息
    Configs: List[type(SubConfigTemplate)] = []
    Widgets: List[ModuleStackPage] = []
    WidgetsLoad: list = []
    Tasks: List[Callable] = []

    ModuleNameCH: str = "未知"  # 模组中文名（用于界面显示和提示信息）
    ModuleNameEN: str = "none"  # 模组英文名（用于路径，关键字，函数名等，避免特殊字符）
    ModuleKey: int = -1  # 识别ID
    IconPath: str = spr.SGAdefaultPic  # 图标路径
    Config: type(SubConfigTemplate)
    Widget: type(ModuleStackPage)
    Task: Callable = defaulttask

    def __init__(self):
        # 每次实例化时，增加计数并将类添加到实例列表中
        if self.LoadModule:
            ModuleClass.Infos.append((self.ModuleNameCH,
                                      self.ModuleNameEN, self.ModuleKey,
                                      self.IconPath))
            ModuleClass.Configs.append(self.Config)
            ModuleClass.Widgets.append(self.Widget)
            ModuleClass.Tasks.append(self.Task)
            ModuleClass.WidgetsLoad.append(False)

    @classmethod
    def GetConfigs(cls) -> List[type(SubConfigTemplate)]:
        return cls.Configs

    @classmethod
    def GetConfig(cls, num: int) -> Optional[SubConfigTemplate]:
        if 0 <= num < len(cls.Configs):
            return cls.Configs[num]()
        return None

    @classmethod
    def GetWidgets(cls):
        return cls.Widgets

    @classmethod
    def GetTasks(cls):
        return cls.Tasks

    @classmethod
    def GetInfos(cls):
        return cls.Infos

    @classmethod
    def GetInfosT(cls) -> List[Tuple]:
        if not cls.Infos:
            return []
        return list(zip(*cls.Infos))

    @classmethod
    def FindItem(cls, _input: [str, int]) -> [list, bool]:
        for n, item in enumerate(cls.Infos):
            if _input in item:
                return list(item) + [n]
        return False

    @classmethod
    def CheckConfig(cls, subconfig: dict):
        modulekey = subconfig.get("ModuleKey", -1)
        if modulekey in cls.GetInfosT()[2]:
            num = cls.FindItem(modulekey)[-1]
            try:
                cls.Configs[num](**subconfig)
                return True
            except Exception as e:
                logger.error(str(e))
        return False
