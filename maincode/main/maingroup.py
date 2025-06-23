from PyQt5.QtCore import QObject, pyqtSignal, pyqtBoundSignal
from maincode.modules.main import ModuleClass, RecognizeModules
from .subconfig import sc, SubConfigs
from .mainconfig import MainConfig, checkmain
from .info import SGAInfo, info
from os import path, makedirs
from typing import Optional
import json
import random


class SGAConfigGroup(QObject):
    infoAdd: pyqtBoundSignal = pyqtSignal(str, bool)
    infoHead: pyqtBoundSignal = pyqtSignal()
    infoEnd: pyqtBoundSignal = pyqtSignal()
    PersonalPath = "./personal"
    MainConfigPath = "./personal/mainconfig.json"
    MainConfigBackupPath = "./personal/mainconfigbackup.json"

    def __init__(self):
        super().__init__()
        self.modules: Optional[ModuleClass] = None
        self.mainconfig: Optional[MainConfig] = None
        self.currentmainconfig: Optional[dict] = None
        self.subconfig: Optional[SubConfigs] = None
        self.info: Optional[SGAInfo] = None

    def Load(self):
        self.modules = ModuleClass
        RecognizeModules()
        self.mainconfig: MainConfig = self.ReadMainConfig()
        self.ReadCurrentConfig()
        self.currentmainconfig: dict = self.mainconfig.model_dump()
        self.subconfig = sc
        if not self.subconfig.filelist:
            self.NewSubFile()
        self.info = info
        self.mainconfig.Version = self.info.Version
        self.SaveMain()
        self.SaveBackUp()
        self.info.BasisFileInit()

    def ReadMainConfig(self):
        # 加载主配置，若损坏则从备份恢复，若备份损坏或没有则进行初始化修复或者初始化
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        _mainconfig = {}
        if path.exists(self.MainConfigPath):
            with open(self.MainConfigPath, 'r', encoding='utf-8') as c:
                _mainconfig = json.load(c)
            if checkmain(_mainconfig):
                return MainConfig(**_mainconfig)
        if path.exists(self.MainConfigBackupPath):
            with open(self.MainConfigBackupPath, 'r', encoding='utf-8') as c:
                _mainconfig: dict = json.load(c)
            if checkmain(_mainconfig):
                self.infoAdd.emit("主配置异常，从备份恢复", False)
                return MainConfig(**_mainconfig)
            else:
                template = MainConfig().model_dump()
                template.update(_mainconfig)
                if checkmain(template):
                    self.infoAdd("主配置异常，进行修复", False)
                    return MainConfig(**template)
        if _mainconfig:
            self.infoAdd.emit("主配置损坏，进行初始化", False)
            return MainConfig()
        else:
            self.infoAdd.emit("主配置初始化", False)
            return MainConfig()

    def ReadCurrentConfig(self):
        _current = self.mainconfig.CurrentConfig
        if _current:
            if self.modules.CheckConfig(_current):
                return
            else:
                self.infoAdd.emit("当前子设置损坏，进行初始化", False)
                self.mainconfig.CurrentConfig = self.modules.GetConfig(0).model_dump()
        else:
            self.infoAdd.emit("进行子设置初始化", False)
            self.mainconfig.CurrentConfig = self.modules.GetConfig(0).model_dump()

    def SaveMain(self):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        _mainconfig = self.mainconfig.model_dump()
        with open(self.MainConfigPath, 'w', encoding='utf-8') as c:
            json.dump(_mainconfig, c, ensure_ascii=False, indent=1)

    def SaveBackUp(self):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        _mainconfig = self.mainconfig.model_dump()
        with open(self.MainConfigBackupPath, 'w', encoding='utf-8') as c:
            json.dump(_mainconfig, c, ensure_ascii=False, indent=1)

    def NewSubFile(self):
        newconfig = self.modules.GetConfig(0)
        while 1:
            ConfigKey = f"{random.randint(0, 9999):04d}"
            if self.modules.FindItem(ConfigKey):
                continue
            else:
                break
        newconfig.ConfigKey = ConfigKey
        self.subconfig.filelist.append((newconfig.ConfigKey,
                                        newconfig.ConfigName,
                                        newconfig.ModuleKey))
        self.subconfig.Save(newconfig.model_dump())

    def ReadSubFile(self, num: int) -> [dict, bool]:
        ck, cn, mk = self.subconfig.filelist[num]
        with open(f"personal/config/{ck + cn}.json", 'r', encoding='utf-8') as c:
            _config = json.load(c)
        if self.modules.CheckConfig(_config):
            return _config
        else:
            return False


sg = SGAConfigGroup()
