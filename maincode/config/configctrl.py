from maincode.tools.classcheck import find_subclasses_of_base, instantiate_class
from maincode.modules.main import ModuleClass
from .subconfig import subconfig, SubConfigs
from .mainconfig import MainConfig, checkmain
from .info import SGAInfo, info
from os import path, makedirs, getcwd
from typing import Optional
import json
import random
import pkgutil
import importlib


class SGAConfigController:
    PersonalPath = "./personal"
    MainConfigPath = "./personal/mainconfig.json"
    MainConfigBackupPath = "./personal/mainconfigbackup.json"

    def __init__(self):
        super().__init__()
        self.modules: Optional[ModuleClass] = None
        self.mc: Optional[MainConfig] = None
        self.currentmainconfig: Optional[dict] = None
        self.sc: Optional[SubConfigs] = None
        self.info: Optional[SGAInfo] = None
        self.loadstate = {"主配置异常，从备份恢复": False,
                          "主配置异常，进行修复": False,
                          "主配置损坏，进行初始化": False,
                          "主配置初始化": False,
                          "当前子设置损坏，进行初始化": False,
                          "进行子设置初始化": False}

    def Load(self):
        self.modules = ModuleClass
        self.mc: MainConfig = self.ReadMainConfig()
        self.RecognizeModules()
        self.ReadCurrentConfig()
        self.currentmainconfig: dict = self.mc.model_dump()
        self.sc = subconfig
        if not self.sc.filelist:
            self.NewSubFile()
        self.info = info
        self.info.OtherConfig = self.mc.OtherConfig
        self.info.OcrPath = self.mc.OcrPath
        self.mc.Version = self.info.Version
        self.SaveMain()
        self.SaveBackUp()
        if self.mc.WorkDir != self.info.Workdir:
            self.info.BasisFileInit()
            self.mc.WorkDir = self.info.Workdir

    def ReadMainConfig(self):
        # 加载主配置，若损坏则从备份恢复，若备份损坏或没有则进行初始化修复或者初始化
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        _mainconfig = {}

        # 尝试加载主配置
        if path.exists(self.MainConfigPath):
            try:
                with open(self.MainConfigPath, 'r', encoding='utf-8') as c:
                    _mainconfig = json.load(c)
                if checkmain(_mainconfig):
                    return MainConfig(**_mainconfig)
            except (json.JSONDecodeError, Exception):
                pass  # 主配置损坏，继续尝试备份

        # 尝试加载备份配置
        if path.exists(self.MainConfigBackupPath):
            try:
                with open(self.MainConfigBackupPath, 'r', encoding='utf-8') as c:
                    _mainconfig = json.load(c)
                if checkmain(_mainconfig):
                    self.loadstate["主配置异常，从备份恢复"] = True
                    return MainConfig(**_mainconfig)
                else:
                    template = MainConfig().model_dump()
                    template.update(_mainconfig)
                    if checkmain(template):
                        self.loadstate["主配置异常，进行修复"] = True
                        return MainConfig(**template)
            except (json.JSONDecodeError, Exception):
                pass  # 备份配置损坏

        # 初始化配置
        if _mainconfig:
            self.loadstate["主配置损坏，进行初始化"] = True
        else:
            self.loadstate["主配置初始化"] = True
        return MainConfig()

    def RecognizeModules(self):
        packagelist = ["maincode", "modules"]
        package = importlib.import_module(".".join(packagelist))
        _l = self.mc.ModulesEnable
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            _list = list(packagelist)
            if ispkg:
                _list.append(modname)
                modulepackage = importlib.import_module(".".join(_list))
                for i, m, p in pkgutil.iter_modules(modulepackage.__path__):
                    if not p and m == "main":
                        _list.append(m)
                        break
                else:
                    continue
                _path = path.join(getcwd(), "/".join(_list)+".py")
                if res := find_subclasses_of_base(_path, "ModuleClass"):
                    class_obj = instantiate_class(_path, res)
                    if class_obj.ModuleNameCH in _l or not _l:
                        class_obj()

    def ReadCurrentConfig(self):
        _current = self.mc.CurrentConfig
        if _current:
            if self.modules.CheckConfig(_current):
                return
            else:
                self.loadstate["当前子设置损坏，进行初始化"] = True
                self.mc.CurrentConfig = self.modules.GetConfig(0).model_dump()
        else:
            self.loadstate["进行子设置初始化"] = True
            self.mc.CurrentConfig = self.modules.GetConfig(0).model_dump()

    def _SaveConfig(self, config_path: str):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        _mainconfig = self.mc.model_dump()
        with open(config_path, 'w', encoding='utf-8') as c:
            json.dump(_mainconfig, c, ensure_ascii=False, indent=1)

    def SaveMain(self):
        self._SaveConfig(self.MainConfigPath)

    def SaveBackUp(self):
        self._SaveConfig(self.MainConfigBackupPath)

    def NewSubFile(self):
        max_attempts = 10000  # 防止无限循环
        attempts = 0
        newconfig = self.modules.GetConfig(0)
        while attempts < max_attempts:
            ConfigKey = f"{random.randint(0, 9999):04d}"
            if self.modules.FindItem(ConfigKey):
                attempts += 1
                continue
            else:
                break
        else:
            raise RuntimeError("无法生成唯一的ConfigKey")
        newconfig.ConfigKey = ConfigKey
        self.sc.filelist.append((newconfig.ConfigKey,
                                 newconfig.ConfigName,
                                 newconfig.ModuleKey))
        self.sc.Save(newconfig.model_dump())

    def ReadSubFile(self, num: int) -> [dict, bool]:
        ck, cn, mk = self.sc.filelist[num]
        with open(f"personal/config/{ck + cn}.json", 'r', encoding='utf-8') as c:
            _config = json.load(c)
        if self.modules.CheckConfig(_config):
            return _config
        else:
            return False


scc = SGAConfigController()
