from os import path, makedirs, listdir
import json
from typing import List, Tuple, Union
import random


class ScheMa(dict):
    def __init__(self, schema: dict):
        super().__init__(schema)

    def typedict(self):
        return {key: _dict['type'] for key, _dict in self.items()}


class ConfigTool(dict):
    ConfigFolderPath = "personal/config"
    ExampleModuleScheMa = {
        'ConfigKey': {'type': str, 'default': ""},  # 每个配置文件的识别码，每个文件唯一
        'ModuleKey': {'type': int, 'default': 0},  # 每个模块的识别码，每个模块唯一
        'ConfigName': {'type': str, 'default': "默认配置"}}  # 每个配置文件的名字，不唯一

    def __init__(self, schema: ScheMa):
        super().__init__()
        self.schema: ScheMa = schema

    def getdefault(self) -> dict:
        """
        根据schema规范生成默认字典
        :return: 包含默认值的字典
        """
        default_dict = {}
        for field, config in self.schema.items():
            if 'default' in config:
                default_dict[field] = config['default']
            elif config.get('required', True):
                # 为必填字段但没有默认值的字段生成默认值
                field_type = config.get('type')
                if field_type == str:
                    default_dict[field] = ""
                elif field_type == int:
                    default_dict[field] = 0
                elif field_type == float:
                    default_dict[field] = 0.0
                elif field_type == bool:
                    default_dict[field] = False
                elif field_type == list:
                    default_dict[field] = []
                elif field_type == dict:
                    default_dict[field] = {}
        return default_dict

    def init(self):
        super().__init__(self.getdefault())

    def GetSelfDict(self):
        return dict(self)

    def check(self, data: dict):
        """
        验证字典是否符合规范
        :param data: 要验证的字典
        :return: (是否有效, 错误信息)
        """
        errors = []
        # 检查必填字段是否缺失
        for field, config in self.schema.items():
            if config.get('required', False) and field not in data:
                errors.append(f"缺少必填字段: {field}")
        # 检查字段类型
        for field, value in data.items():
            if field in self.schema:
                expected_type = self.schema[field].get('type')
                if expected_type and not isinstance(value, expected_type):
                    errors.append(f"字段 '{field}' 类型错误，应为 {expected_type}，实际为 {type(value)}")
        # 检查是否有未定义的字段
        for field in data:
            if field not in self.schema:
                errors.append(f"存在未定义的字段: {field}")
        return len(errors) == 0, errors

    @classmethod
    def save(cls, config: dict):
        if not path.exists(cls.ConfigFolderPath):
            makedirs(cls.ConfigFolderPath)
        configpath = path.join(cls.ConfigFolderPath, config['ConfigKey'] + config['ConfigName'] + ".json")
        with open(configpath, 'w', encoding='utf-8') as c:
            json.dump(config, c, ensure_ascii=False, indent=1)


class SGASubConfigGroup:
    def __init__(self):
        self._configlist: List[ConfigTool] = []
        self._configsignlist: List[Tuple[str, str, int, str]] = []  # 中文名， 英文名， 模组识别码， 图标路径
        self._filelist: List[Tuple[str, str, int]] = []  # 文件识别码， 模组识别码， 文件名

    def SetConfigList(self, configlist: List[ConfigTool]):
        self._configlist = configlist

    def GetConfigList(self):
        return self._configlist

    def SetFileList(self, filelist: List[Tuple[str, str, int]]):
        self._filelist = filelist

    def GetFileList(self):
        return self._filelist

    def GetFileListT(self):
        return tuple(zip(*self._filelist))

    def SetSignListt(self, signlist: List[Tuple[str, str, int, str]]):
        self._configsignlist = signlist

    def GetSignList(self):
        return self._configsignlist

    def GetSignListT(self):
        return tuple(zip(*self._configsignlist))

    def FindSignList(self, _input: Union[str, int]) -> Union[tuple, bool]:
        for item in self._configsignlist:
            for i in item:
                if _input == i:
                    return item
        return False

    def CheckConfig(self, _config: dict) -> bool:
        modulekey = _config.get('ModuleKey', None)
        mklist = list(self.GetSignListT()[2])
        num = mklist.index(modulekey) if modulekey in mklist else -1
        if num >= 0 and self._configlist[num].check(_config):
            return True
        return False

    def LoadSubConfig(self):
        _, _, _, mkl = list(zip(*self._configsignlist))
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
            default = self._configlist[0].getdefault()
            default['ConfigKey'] = f"{random.randint(0, 9999):04d}"
            ConfigTool.save(default)
            _subconfigs = [[default['ConfigKey'],
                            default['ModuleKey'],
                            default['ConfigName']]]
        self._filelist = _subconfigs  # 储存设置文件信息，文件名和类型


class TimerConfig(ConfigTool):
    schema = {
        'ItemNum': {'type': int,         'default': 3},
        'Execute': {'type': list,  'default': [0] * 10},
        'Time':    {'type': list,  'default': [[0, 0]] * 10},
        'Name':    {'type': list,  'default': [''] * 10},
        'Awake':   {'type': list, 'default': [False] * 10},
    }
    schema = ScheMa(schema)

    def __init__(self):
        super().__init__(self.schema)


class SGAMainConfig(ConfigTool):
    tc = TimerConfig()
    schema = {
        'Version': {'type': str, 'default': ''},
        'WorkDir': {'type': str, 'default': ''},
        'OcrPath': {'type': str, 'default': ''},
        'StopKeys': {'type': str, 'default': 'ctrl+/'},
        'AutoUpdate': {'type': bool, 'default': True},
        'TimerConfig': {'type': dict, 'default': tc.getdefault()},
        'ConfigKey': {'type': int, 'default': ''},
        'ConfigLock': {'type': bool, 'default': True},
        'CurrentConfig': {'type': dict, 'default': {}},
        'SubConfig': {'type': dict, 'default': {}},
    }
    schema = ScheMa(schema)
    MainConfigPath = "personal/mainconfig.json"
    MainConfigBackupPath = "personal/mainconfigbackup.json"
    PersonalPath = "personal"

    def __init__(self, sc: SGASubConfigGroup):
        super().__init__(self.schema)
        self.subconfig = sc
        # 加载主配置，若损坏则从备份恢复，若备份损坏或没有则进行初始化修复或者初始化
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        self.configread = False
        self.configmsg = ""
        if path.exists(self.MainConfigPath):
            with open(self.MainConfigPath, 'r', encoding='utf-8') as c:
                _mainconfig = json.load(c)
            if _mainconfig := self.checkmain(_mainconfig):
                self.update(_mainconfig)
                self.configread = True
        if not self.configread and path.exists(self.MainConfigBackupPath):
            with open(self.MainConfigBackupPath, 'r', encoding='utf-8') as c:
                _mainconfig = json.load(c)
            if _mainconfig := self.checkmain(_mainconfig):
                self.update(_mainconfig)
                self.configmsg = "主配置异常，从备份恢复" + self.configmsg
            else:
                self.init()
                self.update(_mainconfig)
                self.configread = True
                self.configmsg = "主配置异常，进行修复" + self.configmsg
        if not self.configread:
            self.configmsg = "主配置初始化" + self.configmsg
            self.init()
            self['CurrentConfig'] = self.subconfig.GetConfigList()[0].getdefault()
        self.configmsg.strip("\n")
        self.savemain()
        self.savebackup()

    def checkmain(self, configdict):
        if self.check(configdict) and self.tc.check(configdict['TimerConfig']):
            pass
        else:
            return False
        subconfig = configdict['CurrentConfig']
        if subconfig:
            if self.subconfig.CheckConfig(subconfig):
                return configdict
            else:
                self.configmsg = "\n子配置损坏,进行重置"
                configdict['CurrentConfig'] = self.subconfig.GetConfigList()[0].getdefault()
                return configdict
        else:
            configdict['CurrentConfig'] = self.subconfig.GetConfigList()[0].getdefault()
            self.configmsg = "\n子配置初始化"
        return configdict

    def keylist(self):
        return list(self.keys())

    def savemain(self):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        with open(self.MainConfigPath, 'w', encoding='utf-8') as c:
            json.dump(dict(self), c, ensure_ascii=False, indent=1)

    def savebackup(self):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        with open(self.MainConfigBackupPath, 'w', encoding='utf-8') as c:
            json.dump(dict(self), c, ensure_ascii=False, indent=1)
