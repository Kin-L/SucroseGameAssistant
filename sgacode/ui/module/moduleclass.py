from typing import Union
from sgacode.tools.myclass import ConfigTool
from typing import List, Tuple
from PyQt5.QtWidgets import QWidget, QFrame
from sgacode.ui.control import palette, ScrollArea, Widget, Stack


class ModuleClass(QWidget):
    Count: int = 0  # 实例化的次数，即模组数量
    Instances: List[object] = []  # 存储所有实例化的类
    SignList: List[Tuple[int, str, str, int]] = []  # 每个实例的以下四项标识信息

    ModuleNum: int = 0  # 序号
    ModuleNameCH: str = ""  # 模组中文名（用于界面显示和提示信息）
    ModuleNameEN: str = ""  # 模组英文名（用于路径，关键字，函数名等，避免特殊字符）
    ModuleKey: int = 0  # 识别ID

    IconPath: str  # 图标路径
    Config: ConfigTool

    scroll: ScrollArea
    widget: Widget

    def __init__(self):
        super().__init__()
        # 每次实例化时，增加计数并将类添加到实例列表中
        ModuleClass.Count += 1
        ModuleClass.Instances.append(self.__class__)
        ModuleClass.SignList.append((self.ModuleNum, self.ModuleNameCH,
                                     self.ModuleNameEN, self.ModuleKey))

    def WidgetInit(self):
        self.setPalette(palette)

        # 功能列表窗口
        self.scroll = ScrollArea((0, 0, 215, 515))
        self.scroll.setFrameShape(QFrame.Shape(0))
        self.widget = Widget((0, 0, 215, 515))
        _wdt = self.widget
        self.scroll.setWidget(_wdt)
        self.widget.setFixedHeight(515)
        self.stack = Stack((225, 0, 395, 515))

    @classmethod
    def CheckConfig(cls, _config: dict):
        modekey = _config.get('ModeKey', None)
        _ins: ModuleClass
        if modekey is not None:
            _ins = cls.FindInstances(modekey)
            if bool(_ins):
                if _ins.Config.check(_config):
                    return True
        return False

    @classmethod
    def GetInstanceCount(cls):
        # 返回实例化的总次数
        return cls.Count

    @classmethod
    def GetInstances(cls):
        # 返回所有实例化的类的名称列表
        return cls.Instances

    @classmethod
    def FindInstances(cls, _input: Union[str, int]) -> Union:
        for item in cls.SignList:
            for i in item:
                if _input == i:
                    return cls.Instances[item[0]]
        return False


class SGAModuleInstances:
    def __init__(self):
        self.Class = ModuleClass
        from sgacode.ui.module.mix import MixClass
        self.Mix = MixClass()

    @staticmethod
    def GetInstances():
        return ModuleClass.Instances

    @staticmethod
    def GetCount():
        return ModuleClass.Count

    @staticmethod
    def GetSignList():
        return ModuleClass.SignList
