from typing import Union
from os import path, makedirs
import json
from sgacode.tools.main import env, ConfigTool, dictlisttype


class QtLocation(tuple):
    def __new__(cls, x: int, y: int, w: int, h: int):
        return super().__new__(cls, (x, y, w, h))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def w(self):
        return self[2]

    @property
    def h(self):
        return self[3]

    @property
    def position(self):
        return self[0], self[1]

    @property
    def size(self):
        return self[2], self[3]


class SGAZone(tuple):
    def __new__(cls, x1: int, y1: int, x2: int, y2: int):
        return super().__new__(cls, (x1, y1, x2, y2))

    @property
    def x1(self):
        return self[0]

    @property
    def y1(self):
        return self[1]

    @property
    def x2(self):
        return self[2]

    @property
    def y2(self):
        return self[3]

    @property
    def position1(self):
        return self[0], self[1]

    @property
    def position2(self):
        return self[2], self[1]

    @property
    def position3(self):
        return self[2], self[3]

    @property
    def position4(self):
        return self[0], self[3]

    @property
    def size(self):
        return self[2] - self[0], self[3] - self[1]

    @property
    def center(self):
        return int((self[2] + self[0])/2), int((self[3] - self[1])/2)


class SGAPosition(tuple):
    def __new__(cls, x: int, y: int):
        return super().__new__(cls, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]


class ScheMa(dict):
    def __init__(self, schema: dict):
        super().__init__(schema)

    def typedict(self):
        return {key: _dict['type'] for key, _dict in self.items()}


class TimerConfig(ConfigTool):
    schema = {
        'ItemNum': {'type': int,         'default': 3},
        'Execute': {'type': [int] * 10,  'default': [0] * 10},
        'Time':    {'type': [str] * 10,  'default': [''] * 10},
        'Name':    {'type': [str] * 10,  'default': [''] * 10},
        'Awake':   {'type': [bool] * 10, 'default': [False] * 10},
    }
    schema = ScheMa(schema)

    def __init__(self):
        super().__init__(self.schema)


class SGASubConfig(ConfigTool):
    schema = {
        'ModeKey':    {'type': str,              'default': 0},
        'ConfigName': {'type': Union[str, None], 'default': None},
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
        'AutoUpdate': {'type': bool, 'default': True},
        'TimerConfig': {'type': TimerConfig, 'default': tc.getdefault()},
        'ConfigName': {'type': str, 'default': ''},
        'ConfigLock': {'type': bool, 'default': True},
        'CurrentConfig': {'type': dict, 'default': {}},
    }
    schema = ScheMa(schema)
    MainConfigPath = "personal/mainconfig.json"
    MainConfigBackupPath = "personal/mainconfigbackup.json"
    PersonalPath = "personal"

    def __init__(self):
        super().__init__(self.schema)
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        env.value["MainConfigBackup"] = False  # 是否从备份文件读取
        env.value["MainConfigTypeChange"] = False  # 主配置文件类型变动
        env.value["MainConfigInit"] = False  # 是否主配置初始化
        configread = False
        if path.exists(self.MainConfigPath):
            with open(self.MainConfigPath, 'r', encoding='utf-8') as c:
                _mainconfig = json.load(c)
            if self.check(_mainconfig):
                self.update(self.schema)
                configread = True
        if not configread and path.exists(self.MainConfigBackupPath):
            with open(self.MainConfigBackupPath, 'r', encoding='utf-8') as c:
                _mainconfig = json.load(c)
            self.update(self.schema)
            configread = False
            env.value["MainConfigBackup"] = True
            if self.check(_mainconfig):
                env.value["MainConfigTypeChange"] = True
        if not configread:
            self.getinit()
            env.value["MainConfigInit"] = True
        self.save()
        self.savebackup()

    def check(self, configdict):
        if self.schema.typedict() != dictlisttype(configdict):
            return False
        if dictlisttype(configdict['TimerConfig']) != TimerConfig.schema.typedict():
            return False
        return True

    def getinit(self):
        return self.update(self.getdefault())

    def keylist(self):
        return list(self.keys())

    def save(self):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        with open(self.MainConfigPath, 'w', encoding='utf-8') as c:
            json.dump(self, c, ensure_ascii=False, indent=1)

    def savebackup(self):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        with open(self.MainConfigBackupPath, 'w', encoding='utf-8') as c:
            json.dump(self, c, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    pass
