import random

from sgacode.configclass import ConfigTool
from typing import Union, List, Tuple
from sgacode.ui.control import ModuleStackPage
from os import path, makedirs, listdir
import json
from sgacode.tools.main import env
from sgacode.configclass import SGAMainConfig


class ModuleClass:
    Count: int = 0  # 实例化的次数，即模组数量
    SignList: List[Tuple[int, str, str, int, str]] = []  # 每个实例的以下四项标识信息

    ModuleNum: int = 0  # 序号
    ModuleNameCH: str = ""  # 模组中文名（用于界面显示和提示信息）
    ModuleNameEN: str = ""  # 模组英文名（用于路径，关键字，函数名等，避免特殊字符）
    ModuleKey: int = 0  # 识别ID

    IconPath: str  # 图标路径
    Config: ConfigTool
    Widget: ModuleStackPage
    PageClass: type(ModuleStackPage)

    def __init__(self):
        super().__init__()
        # 每次实例化时，增加计数并将类添加到实例列表中
        ModuleClass.Count += 1
        ModuleClass.SignList.append((self.ModuleNum, self.ModuleNameCH,
                                     self.ModuleNameEN, self.ModuleKey,
                                     self.IconPath))


class SGAModuleGroup:
    def __init__(self, smc: SGAMainConfig):
        self.Class = ModuleClass
        self.Instances: List[ModuleClass] = []  # 存储所有实例化的类
        # 添加需要载入的模组
        from sgacode.ui.module.mix import MixClass
        self.Instances += [MixClass()]

        # 子设置文件载入
        self.LoadSubConfig()
        if not self.CheckConfig(smc['CurrentConfig']):
            smc['CurrentConfig'] = self.Instances[0].Config.getdefault()

    def LoadSubConfig(self):
        _, _, _, mkl = list(zip(*self.Class.SignList))
        # 读取子设置信息
        _subconfigs = []
        _configdirpath = "personal/config"
        if not path.exists(_configdirpath):
            makedirs(_configdirpath)
        _listdir = listdir(_configdirpath)
        if _listdir:
            for file in _listdir:
                name, suffix = path.splitext(file)
                configkey, name = name[:4], name[4:]
                if suffix == ".json":
                    _path = path.join(_configdirpath, file)
                    with open(_path, 'r', encoding='utf-8') as c:
                        _config = json.load(c)
                        modulekey: Union[int, None] = _config.get("ModuleKey", None)
                    if modulekey is not None:
                        allow = True
                        for item in _subconfigs:
                            if configkey in item and modulekey not in mkl:
                                allow = False
                        if allow:
                            _subconfigs += [[configkey, modulekey, name]]
        if not _subconfigs:
            default = self.Instances[0].Config.getdefault()
            default['ConfigKey'] = f"{random.randint(0, 9999):04d}"
            ConfigTool.save(default)
            _subconfigs = [[default['ConfigKey'],
                            default['ModuleKey'],
                            default['ConfigName']]]
        env.value["SubConfigs"] = _subconfigs  # 储存设置文件信息，文件名和类型

    def GetInstances(self) -> List[ModuleClass]:
        return self.Instances

    @staticmethod
    def GetCount():
        return ModuleClass.Count

    @staticmethod
    def GetSignList():
        return ModuleClass.SignList

    def CheckConfig(self, _config: dict, load: bool = False):
        modulekey = _config.get('ModuleKey', None)
        if modulekey in list(zip(self.GetSignList()))[3]:
            _ins = self.FindInstance(modulekey)
            if _ins and _ins.Config.check(_config):
                if load:
                    _ins.Widget.LoadWindow(_config)
                return True
        return False

    def FindInstance(self, _input: Union[str, int]) -> Union[ModuleClass, bool]:
        for item in ModuleClass.SignList:
            for i in item:
                if _input == i:
                    return self.Instances[item[0]]
        return False

    @staticmethod
    def FindSignList(_input: Union[str, int]) -> Union[tuple, bool]:
        for item in ModuleClass.SignList:
            for i in item:
                if _input == i:
                    return item
        return False

    def LoadWindow(self, moduleconfig: dict):
        mn = self.FindSignList(moduleconfig['ModuleKey'])[0]
        self.Instances[mn].Widget.LoadWindow(moduleconfig)
