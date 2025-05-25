from typing import Union
from sgacode.configclass import ConfigTool
from typing import List, Tuple, Optional
from sgacode.ui.control import Stack, ModuleStackPage
from os import path, makedirs, listdir
import json
from sgacode.tools.main import env
from sgacode.configclass import SGAMainConfig


class ModuleClass:
    Count: int = 0  # 实例化的次数，即模组数量
    Instances: List[object] = []  # 存储所有实例化的类
    SignList: List[Tuple[int, str, str, int]] = []  # 每个实例的以下四项标识信息

    ModuleNum: int = 0  # 序号
    ModuleNameCH: str = ""  # 模组中文名（用于界面显示和提示信息）
    ModuleNameEN: str = ""  # 模组英文名（用于路径，关键字，函数名等，避免特殊字符）
    ModuleKey: int = 0  # 识别ID

    IconPath: str  # 图标路径
    Config: ConfigTool
    Widget: Optional[ModuleStackPage]

    def __init__(self):
        super().__init__()
        self.Widget = None
        # 每次实例化时，增加计数并将类添加到实例列表中
        ModuleClass.Count += 1
        ModuleClass.Instances.append(self)
        ModuleClass.SignList.append((self.ModuleNum, self.ModuleNameCH,
                                     self.ModuleNameEN, self.ModuleKey))

    def WidgetInit(self, stack: Stack):
        pass

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


class SGAModuleGroup:
    def __init__(self, smc: SGAMainConfig):
        self.Class = ModuleClass

        # 添加需要载入的模组
        from sgacode.ui.module.mix import MixClass
        self.Mix = MixClass()

        # 子设置文件载入
        self.LoadSubConfig()
        if not self.Class.CheckConfig(smc['CurrentConfig']):
            smc['CurrentConfig'] = self.Mix.Config.getdefault()

    def LoadSubConfig(self):
        _, _, _, mkl = zip(*self.Class.SignList)
        # 读取子设置信息
        _subconfigs = []
        _configdirpath = "personal/config"
        if not path.exists(_configdirpath):
            makedirs(_configdirpath)
        _listdir = listdir(_configdirpath)
        if _listdir:
            for file in _listdir:
                name, suffix = path.splitext(file)
                seq, name = name[:4], name[4:]
                if suffix == ".json":
                    _path = path.join(_configdirpath, file)
                    with open(_path, 'r', encoding='utf-8') as c:
                        _config = json.load(c)
                        modulekey: Union[int, None] = _config.get("模块", None)
                    if modulekey is not None:
                        allow = True
                        for item in _subconfigs:
                            if seq in item and modulekey not in mkl:
                                allow = False
                        if allow:
                            _subconfigs += [[seq, modulekey, name]]
        env.value["SubConfigs"] = _subconfigs  # 储存设置文件信息，文件名和类型

    @staticmethod
    def GetInstances():
        return ModuleClass.Instances

    @staticmethod
    def GetCount():
        return ModuleClass.Count

    @staticmethod
    def GetSignList():
        return ModuleClass.SignList
